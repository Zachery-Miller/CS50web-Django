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

def index(request):
    # get all posts reverse chronological
    posts = Post.objects.all().order_by('-time_posted')

    return render(request, "network/index.html", {
        "form": NewPostForm(),
        "posts": posts
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

@login_required
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

    return HttpResponseRedirect(reverse("index"))
