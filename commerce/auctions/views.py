from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from auctions.BidForm import BidForm
from auctions.CommentForm import CommentForm

from auctions.ListingForm import ListingForm

from .models import Category, Listing, User, Watchlist


def index(request):
    return render(request, "auctions/index.html")


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

@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {
        "form": form
    })

def index(request):
    active_listings = Listing.objects.filter(status=True)
    return render(request, "auctions/index.html", {
        "listings": active_listings
    })

def listing_view(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    on_watchlist = False
    if request.user.is_authenticated:
        on_watchlist = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    comments = listing.comments.all()
    bid_form = BidForm()
    comment_form = CommentForm()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "on_watchlist": on_watchlist,
        "comments": comments,
        "bid_form": bid_form,
        "comment_form": comment_form
    })

@login_required
def toggle_watchlist(request, listing_id):
    user = request.user
    listing = get_object_or_404(Listing, id=listing_id)
    
    watchlist_item, created = Watchlist.objects.get_or_create(user=user, listing=listing)
    
    if not created:
        watchlist_item.delete()
    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def watchlist(request):
    user = request.user
    watchlist_items = Watchlist.objects.filter(user=user)
    return render(request, "auctions/watchlist.html", {
        "watchlist_items": watchlist_items
    })

@login_required
def submit_bid(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    form = BidForm(request.POST)
    if form.is_valid():
        bid_price = form.cleaned_data['bid_price']
        highest_bid = listing.bids.order_by('-bid_price').first()
        if bid_price < listing.price or (highest_bid and bid_price <= highest_bid.bid_price):
            messages.error(request, "Bid must be higher than the starting bid and any existing bids.")
        else:
            bid = form.save(commit=False)
            bid.user = request.user
            bid.listing = listing
            bid.save()
            messages.success(request, "Your bid has been placed successfully.")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def submit_comment(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.listing = listing
        comment.save()
        messages.success(request, "Your comment has been posted successfully.")
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required
def close_auction(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    if request.user == listing.seller:
        highest_bid = listing.bids.order_by('-bid_price').first()
        if highest_bid:
            listing.winner = highest_bid.user
        listing.status = False
        listing.save()
        messages.success(request, "The auction has been closed.")
    return redirect(reverse("listing", args=[listing_id]))

def categories_view(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

def category_listings_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    listings = category.listings.filter(status=True)
    return render(request, "auctions/category_listings.html", {
        "category": category,
        "listings": listings
    })