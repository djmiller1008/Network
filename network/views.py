import pkgutil
from sqlite3 import connect
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import json 
from .models import PostLike, User, Post, UserFollower



def index(request):
    if request.method == 'POST':
        user = request.user 
        content = request.POST["post-content"]
        post = Post(user=user, content=content)
        post.save()

    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "page_obj": page_obj
    })

@login_required(login_url='login')
def profile(request, username):
    follow_button = False
    following_status = "Follow"
    profile_user = User.objects.get(username=username)
    posts = profile_user.posts.all
    requesting_user = request.user
    if requesting_user != profile_user:
        follow_button = True
        if UserFollower.objects.filter(user=profile_user, follower=requesting_user).count() == 1:
            following_status = "Unfollow"

    followers = profile_user.followers.count()
    following = profile_user.following.count()
    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "user": requesting_user,
        "follow_button": follow_button,
        "followers": followers,
        "following_status": following_status,
        "posts": posts,
        "following": following
    })

@login_required(login_url='login')
def like(request, post_id):
    username = request.user
    user = User.objects.get(username=username)
    post = Post.objects.get(pk=post_id)
    
    if PostLike.objects.filter(user=user, post=post).count() == 0:
        new_postlike = PostLike(user=user, post=post)
        new_postlike.save()
        
        post.likes_number = post.likes_number + 1
        post.save() 
    else:
        post_like = PostLike.objects.get(user=user, post=post)
        post_like.delete()

        post.likes_number = post.likes_number - 1 
        post.save()

    response = {
            1: post.likes_number
        }
    json_string = json.dumps(response)

    return HttpResponse(json_string, content_type="application/json")

def check_for_like(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = User.objects.get(username=request.user) 

    if PostLike.objects.filter(user=user, post=post).count() == 0:
        like_button_text = 'Like'
    else: 
        like_button_text = 'Unlike'
    
    response = {
        1: like_button_text
    }
    json_string = json.dumps(response)
    return HttpResponse(json_string, content_type="application/json")


def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    user = post.user

    if request.user == user:
        edited_post_content = request.POST["post-content"]
        post.content = edited_post_content
        post.save()

        return HttpResponseRedirect(reverse("profile", kwargs={"username": user}))
    

@login_required(login_url='login')
def following(request):
    posts = []
    
    following = request.user.following.all()
    for user in following:
        for post in user.user.posts.all().order_by("-timestamp"):
            posts.append(post)
    
    paginator = Paginator(posts, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })

@login_required(login_url='login')
def toggle_follow(request):
    profile_user = User.objects.get(username=request.POST["profile_user"])
    if request.POST["following_status"] == "Unfollow":
        object = UserFollower.objects.get(user=profile_user, follower=request.user)
        object.delete()
    else:
        followerObject = UserFollower(user=profile_user, follower=request.user)
        followerObject.save()

    return HttpResponseRedirect(reverse("profile", kwargs={'username': profile_user.username}))
        


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
