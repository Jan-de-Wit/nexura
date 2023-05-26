from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Bid, Comment


def index(request):
    listings = Listing.objects.filter(active=True)
    for listing in listings:
        bids = Bid.objects.filter(listing=listing).all()
        highestBid = 0

        for bid in bids:
            highestBid = max(highestBid, bid.bid)

        listing.currentPrice = max(listing.starting_bid, highestBid)

    return render(request, "auctions/index.html", {
        "listings": listings,
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listing(request):
    if request.method == "GET":
        return render(request, "auctions/create_listing.html")

    try:
        listing = Listing(
            title=request.POST["title"],
            description=request.POST["description"],
            starting_bid=float(request.POST["starting_bid"]),
            category=request.POST["category"],
            image=request.POST["image"],
            created_by=request.user,
            active=True
        )
    except ValueError as e:
        return render(request, "auctions/create_listing.html", {
            "message": f"One or more fields are not valid.<br><p style='color: red;'>Error: {e}</p>",
        })

    try:
        listing.full_clean()
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    except ValidationError as e:
        return render(request, "auctions/create_listing.html", {
            "message": f"One or more fields are not valid.<br><p style='color: red;'>Error: {e}</p>",
            "listing": listing,
        })


def view_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listing).order_by('created_on').all()
    highestBid = 0

    for bid in bids:
        highestBid = max(highestBid, bid.bid)

    comments = Comment.objects.filter(listing=listing).order_by('created_on').all()
    onWatchlist = request.session.get("watchlist", False)

    if onWatchlist:
        onWatchlist = listing_id in onWatchlist

    listing.currentPrice = max(listing.starting_bid, highestBid)

    return render(request, "auctions/view_listing.html", {
        "listing": listing,
        "bids": bids,
        "comments": comments,
        "onWatchlist": onWatchlist,
    })


def manipulateWatchlist(request, listing_id):
    watchlist = request.session.get("watchlist", False)

    if watchlist:
        if listing_id in watchlist:
            watchlist.remove(listing_id)
        else:
            watchlist.append(listing_id)
    else:
        watchlist = [listing_id]

    request.session["watchlist"] = watchlist
    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))


def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if listing.created_by == request.user:
        highestBid = Bid.objects.filter(listing=listing).order_by('-bid').first()

        if highestBid:
            listing.winner = highestBid.user

        listing.active = False
        listing.save()

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))


def bid(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bid = float(request.POST["bid"])

    bids = Bid.objects.filter(listing=listing).all()
    highestBid = 0

    for dbBid in bids:
        highestBid = max(highestBid, dbBid.bid)

    if bid >= highestBid:
        bid = Bid(
            listing=listing,
            user=request.user,
            bid=bid,
        )
        bid.save()
    else:
        listing.currentPrice = highestBid
        return render(request, "auctions/view_listing.html", {
            "listing": listing,
            "bids": bids,
            "message": "Bid must be higher than the current highest bid.",
        })

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))

def comment(request, listing_id):
    if not request.user.is_authenticated or request.POST.get("comment", "") == "":
        return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))
    
    listing = Listing.objects.get(pk=listing_id)
    comment = request.POST["comment"]

    comment = Comment(
        listing=listing,
        user=request.user,
        comment=comment,
    )
    comment.save()

    return HttpResponseRedirect(reverse("view_listing", args=(listing_id,)))

@login_required
def watchlist(request):
    watchlist = request.session.get("watchlist", False)
    listings = []

    if watchlist:
        for listing_id in watchlist:
            listing = Listing.objects.get(pk=listing_id)
            bids = Bid.objects.filter(listing=listing).all()
            highestBid = 0

            for bid in bids:
                highestBid = max(highestBid, bid.bid)

            listing.currentPrice = max(listing.starting_bid, highestBid)
            listings.append(listing)

    return render(request, "auctions/watchlist.html", {
        "listings": listings,
    })

def categories(request, category):
    listings = Listing.objects.filter(category=category, active=True)
    for listing in listings:
        bids = Bid.objects.filter(listing=listing).all()
        highestBid = 0

        for bid in bids:
            highestBid = max(highestBid, bid.bid)

        listing.currentPrice = max(listing.starting_bid, highestBid)

    return render(request, "auctions/category.html", {
        "listings": listings,
        "category": category,
    })

def allCategories(request):
    categories = Listing.objects.values('category').all()
    categoriesSet = set()

    for category in categories:
        if category.get("category", None) != '' and category is not None:
            categoriesSet.add(category.get('category', 'None'))

    return render(request, "auctions/allCategories.html", {
        "categories": categoriesSet,
    })