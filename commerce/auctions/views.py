from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm

from .models import User, Listing

'''FORMS'''
# listing form
class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'category', 'image_URL']

# active listings page
def index(request):
    return render(request, "auctions/index.html")

@login_required(login_url="login")
def create_listing(request):
    if request.method == "POST":
        pass

    else:
        return render(request, "auctions/new_listing.html")

def listing(request, listing_id):
    # break this into GET and POST sections
    # if signed in, be able to add/remove from watchlist
    # if signed in, be able to bid - bid must be larger than current price. present error otherwise (reverse the page and add an error up top)
    # if signed in and you are the user that created listing, be able to close listing (Listing.active = False)
    # if listing is closed and user is signed in present whether or not they have won the auction
    # if listing is active and if user is signed in allow comments to be added
    pass

def watchlist(request):
    pass

def categories(request):
    pass

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
