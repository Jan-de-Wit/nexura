import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import Follows, Post, User


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_protect
def create_post(request):
    if request.method == "POST":
        try:
            post_data = json.loads(request.body.decode("utf-8"))
            content = post_data.get("content", "")

            if content == "":
                return JsonResponse({"message": "Post Content Required.", "status_code": 400}, status=400)

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User must be logged in.", "status_code": 400}, status=400)

            post = Post(content=content, user=user)
            post.save()
        except Exception as e:
            return JsonResponse({"message": e, "status_code": 400}, status=400)
        return JsonResponse({"message": "Post Created Successfully.", "status_code": 200}, status=200)
    else:
        return JsonResponse({"message": "POST Request Required.", "status_code": 400}, status=400)


def view_posts(request):
    if request.method == "POST":
        try:
            page_number = request.GET.get("page", 1)
            posts = Post.objects.all().order_by("-timestamp")

            paginator = Paginator(posts, 10)
            page = paginator.get_page(page_number)
            serialized_posts = [post.serialize() for post in page]
            response = {
                "posts": serialized_posts,
                "num_pages": paginator.num_pages,
                "has_previous": page.has_previous(),
                "previous_page_number": page.previous_page_number() if page.has_previous() else None,
                "has_next": page.has_next(),
                "next_page_number": page.next_page_number() if page.has_next() else None,
                "status_code": 200
            }

            return JsonResponse(response, safe=False, status=200)
        except Exception as e:
            return JsonResponse({"message": str(e), "status_code": 400}, status=400)
    else:
        return JsonResponse({"message": "POST Request Required.", "status_code": 400}, status=400)


def set_follow_status(request, user_id):
    if request.method == "PUT":
        try:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User must be logged in.", "status_code": 400}, status=400)

            if user.id == user_id:
                return JsonResponse({"message": "User cannot follow themselves.", "status_code": 400}, status=400)

            is_following = Follows.objects.filter(
                user=user, following=user_id).first()

            if is_following is None:
                is_following = False
            else:
                is_following = True

            user_to_follow = User.objects.get(id=user_id)
            if not is_following:
                follow = Follows(user=user, following=user_to_follow)
                follow.save()
            else:
                Follows.objects.filter(
                    user=user, following=user_to_follow).delete()

        except Exception as e:
            return JsonResponse({"message": e, "status_code": 400}, status=400)

        return JsonResponse({"message": "Follow Status Updated Successfully.", "status_code": 200, "is_following": True if is_following else False}, status=200)
    else:
        return JsonResponse({"message": "PUT Request Required.", "status_code": 400}, status=400)


def view_profile(response, user_id):
    if response.method == "GET":
        try:
            profile = User.objects.get(id=user_id)
            is_following = Follows.objects.filter(
                user=response.user, following=user_id).first()

            if is_following is None:
                is_following = False
            else:
                is_following = True

            return render(response, "network/profile.html", {"profile": profile.serialize(), "status_code": 200, "is_following": is_following})
        except Exception as e:
            return JsonResponse({"message": e, "status_code": 400}, status=400)
    else:
        return JsonResponse({"message": "GET Request Required.", "status_code": 400}, status=400)


def view_posts_by_user(request, user_id):
    if request.method == "POST":
        try:
            if not User.objects.filter(id=user_id).exists():
                return JsonResponse({"message": "User does not exist.", "status_code": 400}, status=400)

            posts = Post.objects.filter(user=user_id).order_by("-timestamp")

            page_number = request.GET.get("page", 1)
            paginator = Paginator(posts, 10)
            page_obj = paginator.get_page(page_number)

            serialized_posts = [post.serialize() for post in page_obj]
            return JsonResponse(
                {
                    "posts": serialized_posts,
                    "status_code": 200,
                    "num_pages": paginator.num_pages,
                    "has_previous": page_obj.has_previous(),
                    "has_next": page_obj.has_next(),
                    "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
                    "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
                },
                safe=False,
                status=200,
            )
        except Exception as e:
            return JsonResponse({"message": str(e), "status_code": 400}, status=400)
    else:
        return JsonResponse({"message": "POST Request Required.", "status_code": 400}, status=400)


@login_required
def view_following(request):
    return render(request, "network/following.html")


@login_required
def get_following_posts(request):
    if request.method == "POST":
        try:
            following_ids = Follows.objects.filter(
                user=request.user).values_list("following", flat=True)
            posts = Post.objects.filter(
                user__id__in=following_ids).order_by("-timestamp")

            paginator = Paginator(posts, 10)
            page_number = request.GET.get("page")
            page_obj = paginator.get_page(page_number)

            serialized_posts = [post.serialize() for post in page_obj]

            return JsonResponse(
                {
                    "posts": serialized_posts,
                    "status_code": 200,
                    "num_pages": paginator.num_pages,
                    "has_previous": page_obj.has_previous(),
                    "has_next": page_obj.has_next(),
                    "previous_page_number": page_obj.previous_page_number() if page_obj.has_previous() else None,
                    "next_page_number": page_obj.next_page_number() if page_obj.has_next() else None,
                },
                safe=False,
                status=200,
            )
        except Exception as e:
            return JsonResponse({"message": str(e), "status_code": 400}, status=400)
    else:
        return JsonResponse({"message": "POST Request Required.", "status_code": 400}, status=400)


def update_post(request, post_id):
    if request.method == "PUT":
        try:
            post_data = json.loads(request.body.decode("utf-8"))
            content = post_data.get("content", "")

            if content == "":
                return JsonResponse({"message": "Post Content Required.", "status_code": 400}, status=400)

            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User must be logged in.", "status_code": 400}, status=400)

            post = Post.objects.get(id=post_id)
            if post.user != user:
                return JsonResponse({"message": "User cannot update another user's post.", "status_code": 400}, status=400)

            post.content = content
            post.save()
        except Exception as e:
            return JsonResponse({"message": e, "status_code": 400}, status=400)
        return JsonResponse({"message": "Post Updated Successfully.", "content": content, "status_code": 200}, status=200)
    else:
        return JsonResponse({"message": "PUT Request Required.", "status_code": 400}, status=400)


def set_like_status(request, post_id):
    if request.method == "PUT":
        try:
            user = request.user
            if not user.is_authenticated:
                return JsonResponse({"message": "User must be logged in.", "status_code": 400}, status=400)

            post = Post.objects.get(id=post_id)
            is_liked = post.likes.filter(id=user.id).exists()
            if not is_liked:
                post.likes.add(user)
            else:
                post.likes.remove(user)
        except Exception as e:
            return JsonResponse({"message": e, "status_code": 400}, status=400)

        return JsonResponse({"message": "Like Status Updated Successfully.", "status_code": 200, "is_liked": True if not is_liked else False, "like_count": post.likes.count()}, status=200)
    else:
        return JsonResponse({"message": "PUT Request Required.", "status_code": 400}, status=400)
