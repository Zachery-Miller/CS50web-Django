from xml.etree.ElementTree import Comment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist

from .models import Bid, User, Listing, Comment, Watchlist

'''FORMS'''
# listing form
class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'image_URL']

# comment form
class NewCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

# bid form
class NewBidForm(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']

# active listings page
def index(request):
    active_listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html",{
        "active_listings": active_listings
    })

@login_required(login_url="auctions:login")
def create_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)

        # server-side form validation
        if form.is_valid():
            # get form data
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            category = form.cleaned_data["category"]
            image_URL = form.cleaned_data["image_URL"]

            # create new listing instance
            new_listing = Listing(
                title = title,
                description = description,
                price = price,
                category = category,
                image_URL = image_URL,
                creator = User.objects.get(pk=request.user.id)
            )

            # save new listing
            new_listing.save()

            # return to homepage (WANT THIS TO BE USERS LISTINGS PAGE ONCE THAT IS COMPLETE)
            return HttpResponseRedirect(reverse("auctions:index"))

        
        # invalid form, refresh page with error msg
        else:
            return render(request, "auctions/new_listing.html", {
                "form": form,
                "message": "Form submission invalid. Please check all fields and resubmit."
            })

    else:
        return render(request, "auctions/new_listing.html", {
            "form": NewListingForm()
        })

def listing(request, listing_id):
    # handle improper method
    if request.method == "POST":    
        return render(request, "auctions/error.html", {
            "code": 405,
            "message": "Request method 'POST' not allowed at this address."
        })

    # check if listing exists
    try:
        listing = Listing.objects.get(pk=listing_id)

    except ObjectDoesNotExist:
        return render(request, "auctions/error.html", {
            "code": 404,
            "message": "Auction Does Not Exist"
        })

    # check if listing is active
    if listing.active == True:
        # check if user is logged in and get watchlist info
        if request.user.is_authenticated:
            watchlist = Watchlist.objects.filter(
                listing = listing,
                watcher = User.objects.get(pk=request.user.id)
            ).first()

            # check if item is on watchlist
            if watchlist is not None:
                watching = True
            else:
                watching = False
        else:
            watching = False
        
        # get comments
        comments = Comment.objects.filter(listing=listing_id)

    # if listing is closed
    else:
        pass
        # return listing closed

    # display page since GET was used
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watching": watching,
        "comments": comments,
        "bid_form": NewBidForm(),
        "comment_form": NewCommentForm()
    })

def add_to_watchlist(request, listing_id):
    # create new Watchlist instance
    watchlist = Watchlist(
        listing = Listing.objects.get(pk=listing_id),
        watcher = User.objects.get(pk=request.user.id)
    )

    # save
    watchlist.save()

    # return to listing page
    return HttpResponseRedirect(reverse("auctions:listing", args=(int(listing_id),)))


def remove_from_watchlist(request, listing_id):
    # filter Watchlist objects
    watchlist = Watchlist.objects.filter(
        listing = Listing.objects.get(pk=listing_id),
        watcher = User.objects.get(pk=request.user.id)
    ).first()

    # attempt to delete object
    if watchlist is not None:
        watchlist.delete()
    else:
        return HttpResponseRedirect(reverse("auctions:listing", args=(int(listing_id),)))
    
    # return to listing page
    return HttpResponseRedirect(reverse("auctions:listing", args=(int(listing_id),)))


'''
@login_required(login_url="auctions:login")
def watchlist(request):
    watched_listings = Listing.objects.filter(active=True)

    return render(request, "auctions/index.html",{
        "active_listings": active_listings
    })
'''

def categories(request):
    pass

def new_bid(request, listing_id):
    # check if listing exists
    try:
        listing = Listing.objects.get(pk=listing_id)
        current_price = listing.price

    except ObjectDoesNotExist:
        return render(request, "auctions/error.html", {
            "code": 404,
            "message": "Auction Does Not Exist"
        })

    # handle post request data    
    if request.method == "POST":
        form = NewBidForm(request.POST)

        # server-side form validation
        if form.is_valid():
            # get form data
            bid = form.cleaned_data["bid_amount"]
        
        # invalid form, refresh page --with error msg if possible
        else:
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

        # bid is less than or equal to current price
        if bid <= current_price:
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))
        
        # bid is greater than current price
        elif bid > current_price:
            # create a new bid instance
            new_bid = Bid(
                listing = listing,
                bid_amount = bid,
                bidder = User.objects.get(pk=request.user.id)
            )

            # save new bid and update current price
            new_bid.save()
            listing.price = bid
            listing.save()

            # return to listing page
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

    # handle improperly accessing route
    if request.method == "GET":
        return render(request, "auctions/error.html", {
            "code": 405,
            "message": "Request method 'GET' not allowed at this address."
        })


def new_comment(request, listing_id):
    # check if listing exists
    try:
        listing = Listing.objects.get(pk=listing_id)

    except ObjectDoesNotExist:
        return render(request, "auctions/error.html", {
            "code": 404,
            "message": "Auction Does Not Exist"
        })

    # handle post request data    
    if request.method == "POST":
        form = NewCommentForm(request.POST)

        # server-side form validation
        if form.is_valid():
            # get form data
            comment = form.cleaned_data["comment"]
        
        # invalid form, refresh page --with error msg if possible
        else:
            return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

        # create a new comment instance
        new_comment = Comment(
            listing = listing,
            comment = comment,
            commenter = User.objects.get(pk=request.user.id)
        )

        # save new comment
        new_comment.save()

        # return to listing page
        return HttpResponseRedirect(reverse("auctions:listing", args=(listing.id,)))

    # handle improperly accessing route
    if request.method == "GET":
        return render(request, "auctions/error.html", {
            "code": 405,
            "message": "Request method 'GET' not allowed at this address."
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
