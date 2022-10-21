import json
from typing import Text
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.forms import ModelForm, Textarea
from django.contrib.auth.decorators import login_required

from .models import User, Post, Like, Follow

# new post form
class NewPostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


def home(request):
    # get all posts reverse chronological from users the logged in user is following
    active_user = User.objects.get(pk=request.user.id)
    following_ids = active_user.follower.all().values_list('following', flat=True)
    posts = Post.objects.filter(poster__id__in=following_ids).order_by('-time_posted')
    serialized_posts = get_serialized(request, posts)

    return render(request, "network/home.html", {
        "form": NewPostForm(),
        "posts": serialized_posts
    })

def explore(request):
    # get all posts reverse chronological
    posts = Post.objects.all().order_by('-time_posted')
    serialized_posts = get_serialized(request, posts)

    return render(request, "network/explore.html", {
        "posts": serialized_posts
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
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("explore"))


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
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "network/register.html")

@login_required(login_url="login")
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"message": "Incorrect method."}, status=405)

    poster = User.objects.get(pk=request.user.id)
    form = NewPostForm(request.POST)

    # server-side form validation
    if form.is_valid():
        # get form data
        content = form.cleaned_data["content"]

        # create new post instance
        new_post = Post(
            poster = poster,
            content = content
        )

        # save new post
        new_post.save()

    return HttpResponseRedirect(reverse("profile", args=[poster.username]))

def profile_page(request, profile_user_username):
    # get info about user whose profile is being viewed
    profile_user = User.objects.get(username=profile_user_username)
    following_count = Follow.objects.filter(follower=profile_user).count()
    followed_by_count = Follow.objects.filter(following=profile_user).count()
    posts = Post.objects.filter(poster=profile_user).order_by('-time_posted')
    serialized_posts = get_serialized(request, posts)

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "following": following_count,
        "followers": followed_by_count,
        "posts": serialized_posts
    })

def follow(request, profile_user_username):
    following = User.objects.get(username=profile_user_username)
    follower = User.objects.get(pk=request.user.id)

    if Follow.objects.filter(follower=follower).filter(following=following).exists():
        return JsonResponse({"message": "Already following user."}, status=406)
    else:
        new_follow = Follow.objects.create(follower=follower, following=following)
        new_follow.save()

        return JsonResponse({"message": f"{follower} followed {following}."}, status=200)


def unfollow(request, profile_user_username):
    following = User.objects.get(username=profile_user_username)
    follower = User.objects.get(pk=request.user.id)

    if Follow.objects.filter(follower=follower).filter(following=following).exists():
        Follow.objects.filter(follower=follower).filter(following=following).first().delete()
        return JsonResponse({"message": f"{follower} unfollowed {following}."}, status=200)
    else:
        return JsonResponse({"message": "You aren't following this user."}, status=406)

def check_follow_status(request, profile_user):
    if request.method != "GET":
        return JsonResponse({"message": "Incorrect method."}, status=405)

    following = User.objects.get(username=profile_user)
    follower = User.objects.get(pk=request.user.id)

    if Follow.objects.filter(follower=follower).filter(following=following).exists():
        return JsonResponse({"following": True}, status=200)
    else:
        return JsonResponse({"following": False}, status=200)
    
@login_required(login_url="login")
def toggle_like(request, post_id):
    post = Post.objects.get(id=post_id)

    if Like.objects.filter(post=post).filter(user=request.user).exists():
        like = Like.objects.filter(post=post).filter(user=request.user).first().delete()
        post.likes -= 1
        message = "Like removed"
        
    else:
        like = Like.objects.create(post=post, user=request.user)
        like.save()
        post.likes += 1
        message = "Like created"
        
    post.save()
    return JsonResponse({"message": message}, status=200)

@login_required(login_url="login")
def edit_post(request, post_id): 
    if request.method == "POST":
        post = Post.objects.get(id=post_id)

        # get data from post request
        data = json.loads(request.body)
        edited_content = data.get("new_content")

        # update content and save post
        post.content = edited_content
        post.save()

        return JsonResponse({"message": "Post has been edited."}, status=200)

    else:
        return JsonResponse({"message": "Incorrect method."}, status=405)

@login_required(login_url="login")
def delete_post(request, post_id): 
    if request.method == "POST":
        post = Post.objects.get(id=post_id)
        post.delete()

        return JsonResponse({"message": "Post has been deleted."}, status=200)

    else:
        return JsonResponse({"message": "Incorrect method."}, status=405)

# non request-based or API functions
def get_serialized(request, posts):
    serialized_posts = []
    for post in posts:
        if request.user.is_authenticated:
            if Like.objects.filter(user=request.user, post=post).exists():
                liked = True
            else:
                liked = False
        else:
            liked = False
        
        serialized_post = post.serialize_post(liked)
        serialized_posts.append(serialized_post)
    
    return serialized_posts