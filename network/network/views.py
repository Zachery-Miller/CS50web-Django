import json
from sqlite3 import Timestamp
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Like, Profile


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

        # Attempt to create new user and profile
        try:
            user = User.objects.create_user(username, email, password)
            user.save()

            profile = Profile(
                user=user
            )
            profile.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def show_posts(request, page):
    # route can only be accessed via GET
    if request.method != "GET":
        return JsonResponse({"error": "GET method required."}, status=405)

    # get all posts that exist and return them in reverse chronological order
    if page == "all-posts":
        posts = Post.objects.all().order_by('-timestamp')

        return JsonResponse([post.serialize() for post in posts], safe=False)

    elif page == "following-posts":
        pass

    else:
        return JsonResponse({"error": "Not a valid page."}, status=400)

def toggle_like(request):
    pass

def toggle_follow(request, user):
    # GET active user and profile user info
    if request.method == "GET":
        active_user = User.objects.get(pk=request.user.id)
        profile_user = User.objects.get(username=user)
        profile_user_profile = Profile.objects.get(user=profile_user)

        # check if any follow relationship exists in the direction (active_user -> profile_user)
        if Profile.objects.filter(followed_by=active_user).filter(user=profile_user).exists():
            # return following = True
            return JsonResponse({"following": True}, status=200)
        else:
            # return following = False
            return JsonResponse({"following": False}, status=200)

def profile_page(request, user):
    # if accessed via GET
    if request.method == "GET":
        # try to find user
        try:
            profile_user = User.objects.get(username=user)
            profile_user_profile = Profile.objects.get(user=profile_user)
        except User.DoesNotExist:
            return render(request, "network/error.html", {
                "error": f"User '{user}' does not exist.",
                "status": 404
            })
        
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "following_count": profile_user_profile.user.following.count(),
        "follower_count": profile_user_profile.followed_by.count()
    })

@csrf_exempt
@login_required
def new_post(request):
    # route can only be accessed via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST method required."}, status=405)

    # load form data
    data = json.loads(request.body)
    content = data.get("content")

    # if no content
    if content == "":
        return JsonResponse({"error": "Need content to submit to post."}, status=400)

    # add post to db
    post = Post(
        poster=User.objects.get(pk=request.user.id),
        content=content
    )
    post.save()
    
    return JsonResponse({"message": "successful post"}, status=201)