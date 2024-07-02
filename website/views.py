from datetime import datetime
import json
import os
from django.db import IntegrityError
from django.http import FileResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Track
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File

from audiocraft.models import MusicGen
from audiocraft.data.audio import audio_write


@login_required
def index(request):
    return render(request, "website/index.html")


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        user = authenticate(request, username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "website/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "website/login.html")


def register_view(request):
    if request.method == "POST":
        username = request.POST["username"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "website/register.html", {
                "message": "Passwords must match."
            })

        try:
            user = User.objects.create_user(username, username, password)
            user.save()
        except IntegrityError:
            return render(request, "website/register.html", {
                "message": "Username is unavailable."
            })
        except:
            return render(request, "website/register.html", {
                "message": f"Something went wrong. Please try again later.",
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "website/register.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


@login_required
def view_recent_tracks(request):
    if result := Track.objects.filter(owner=request.user).all().order_by("-created_on"):
        return render(request, "website/recent_tracks.html", {
            "tracks": json.dumps([track.serialize() for track in result]),
        })

    return render(request, "website/recent_tracks.html", {
        "tracks": [],
    })

@login_required
def get_recent_tracks(request):
    if request.method == "POST" and request.user.is_authenticated:
        if result := Track.objects.filter(owner=request.user).all().order_by("-created_on"):
            return JsonResponse({"status": "Success", "tracks": [track.serialize() for track in result]}, status=200)

        return JsonResponse({"status": "Failed", "message": "No tracks found."}, status=404)

    return JsonResponse({"status": "Failed", "message": "POST request required."}, status=405)


def get_track(request, track_id):
    track = Track.objects.filter(id=track_id).first()
    if track:
        file_path = track.track.path
        return FileResponse(open(file_path, "rb"))
    else:
        return JsonResponse({"status": "Failed", "message": "Track not found"}, status=404)



def view_search(request):
    return render(request, "website/search.html")


@csrf_exempt
def generate_from_prompt(request):
    if request.method == "POST" and request.user.is_authenticated:
        print("Loading model")
        model = MusicGen.get_pretrained("small", "cuda")
        print("Loaded model\nSetting generation params")
        model.set_generation_params(duration=30)

        prompt = json.loads(request.body).get("prompt", None)
        if prompt is None or prompt.strip() == "":
            return JsonResponse({"status": "Failed", "error": "Prompt required."}, status=400)

        print(f"Generating: {[prompt]}")

        audio = model.generate([prompt], progress=True)

        print("Generated prompt")
        print("Creating track")

        try:
            for idx, one_wav in enumerate(audio):
                file_path = f"media/{idx}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}"
                print(f"Writing audio to: {file_path}")
                returned_file_path = audio_write(file_path, one_wav, model.sample_rate, "wav")

            if returned_file_path is None:
                os.remove(file_path)
                return JsonResponse({"status": "Failed", "error": "Something went wrong while saving the audio. Please try again later."}, status=500)
            
            print(f"Saved audio to {returned_file_path}")
            
            with open(returned_file_path, 'rb') as f:
                track = Track(owner=request.user, prompt=prompt, track=File(f))
                track.save()

        except Exception as e:
            print(f"Error saving track: {e}")
            os.remove(f"{os.getcwd()}/{file_path}.wav")
            
            return JsonResponse({"status": "Failed", "error": "Failed to save the track to the database. Please try again later."}, status=500)

        os.remove(f"{os.getcwd()}\\{file_path}.wav")
        print(track)
        print(file_path)

        return JsonResponse({"status": "Success", "track": track.serialize()}, status=200)
    else:
        return JsonResponse({"status": "Failed", "error": "POST request required."}, status=405)
    
@login_required
def get_search_results(request):
    if request.method == "POST" and request.user.is_authenticated:
        result = None
        print(request)

        print(request.body)
        print(request.POST)

        query = json.loads(request.body).get("query", None)
        if query is None or query.strip() == "":
            return JsonResponse({"status": "Failed", "error": "Query required."}, status=400)

        result = Track.objects.filter(
            prompt__contains=query).all().order_by('-created_on')

        if result:
            return JsonResponse({"status": "Success", "count": len(result), "result": [track.serialize() for track in result]}, status=200)

        return JsonResponse({"status": "Failed", "message": "No tracks found."}, status=404)

    return JsonResponse({"status": "Failed", "message": "POST request required."}, status=405)
