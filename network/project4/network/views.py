import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from yaml import serialize, serialize_all
from django.core.paginator import Paginator

from .models import Post, User, Profile


def index(request):

    if request.user.is_authenticated:
       user_logged = request.user
       v_user = User.objects.filter(username=user_logged)
       profiles = Profile.objects.filter(user__in=v_user)

       #verify created profile, else force create
       if profiles.count() <= 0:                    
          profile = Profile(                
                user=request.user,
                age=0,
                gender="" )
          profile.save()

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

@csrf_exempt
def posts(request):

    if request.method != "POST" and request.method != "GET":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    if request.method == "POST" and request.user.is_authenticated:

        if not request.user.is_authenticated :
           return JsonResponse({"error": "Unauthenticated."}, status=404)

        data = json.loads(request.body)

        content = data.get("content", "")

        post = Post(
            content=content,
            user=request.user
        )
        post.save()

        return JsonResponse({"message": "Post sent successfully."}, status=201)    

    if request.method == "GET":

        try:
            posts = Post.objects.all()     
            posts = posts.order_by("-created").all()     
            paginator = Paginator(posts,10)  
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number)                  
        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
        

        return JsonResponse({"posts":[post.serialize() for post in posts],
                            "page": {
                                "current": posts.number,
                                "has_next": posts.has_next(),
                                "has_previous": posts.has_previous(),
                            },
                             "user_auth": request.user.username}, safe=False)


@csrf_exempt
def profile(request,user_profile):
   
        try:
            v_user = User.objects.filter(username=user_profile)
            profiles = Profile.objects.filter(user__in=v_user)
            posts = Post.objects.filter(user__in=v_user)     
            posts = posts.order_by("-created").all()   
            
            paginator = Paginator(posts,10)  
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number) 
                
        except Profile.DoesNotExist:
            return JsonResponse({"error": "Profile not found."}, status=404)
              
        return JsonResponse({"profile": [profile.serialize() for profile in profiles],
                             "posts": [post.serialize() for post in posts], 
                             "page": {
                                "current": posts.number,
                                "has_next": posts.has_next(),
                                "has_previous": posts.has_previous(),
                            },                            
                             "user_auth": request.user.username }, safe=False)


@csrf_exempt
@login_required
def following_posts(request):
   
        try:
            user = User.objects.filter(username=request.user)

            lst = []
            profiles = Profile.objects.filter(followers__in=user)
            for profile in profiles:                
                lst.append(profile.user)

            posts = Post.objects.filter(user__in=lst)    

            paginator = Paginator(posts,10)  
            page_number = request.GET.get('page')
            posts = paginator.get_page(page_number) 

        except Post.DoesNotExist:
            return JsonResponse({"error": "Post not found."}, status=404)
              
        return JsonResponse({"posts":[post.serialize() for post in posts],
                             "page": {
                                "current": posts.number,
                                "has_next": posts.has_next(),
                                "has_previous": posts.has_previous(),
                            },
                             "user_auth": request.user.username}, safe=False)   

@csrf_exempt
@login_required
def follow(request, user_profile):
   
    if request.method == "PUT":

        data = json.loads(request.body)

        content = data.get("follow", "")

        user_logged = request.user

        if (content=="Y"):
            
            v_user = User.objects.get(username=user_profile)
            profile = Profile.objects.get(user=v_user)
            profile.followers.add(user_logged)
            profile.save() 
        
        else :
        
            v_user = User.objects.get(username=user_profile)
            profile = Profile.objects.get(user=v_user)
           
            profile.followers.remove(user_logged)
            profile.save() 
                  
        return JsonResponse({"message": "success"}, status=201)   
            
    else:
            return JsonResponse({
                "error": "PUT request required."
            }, status=400)   


@csrf_exempt
@login_required
def like(request, post_id):
   
    if request.method == "PUT":

        data = json.loads(request.body)

        content = data.get("like", "")

        user_logged = request.user

        post = Post.objects.get(id=post_id)
        if (content=="Y"):
            post.likes.add(user_logged)
        else:
            post.likes.remove(user_logged)
        post.save()

        count_likes = post.likes.all().count()
                  
        return JsonResponse({"message": "success", "count_likes":count_likes}, status=201)   
            
    else:
            return JsonResponse({
                "error": "PUT request required."
            }, status=400)       


@csrf_exempt
@login_required
def edit_post(request, post_id):
   
    if request.method == "POST":

        data = json.loads(request.body)

        content = data.get("content", "")

        user_logged = request.user

        post = Post.objects.get(id=post_id)

        if post.user != user_logged:
            return JsonResponse({
                "error": "Invalid user."
            }, status=400)  
        
        post.content = content
        post.save()
                  
        return JsonResponse({"message": "success"}, status=201)   
            
    else:
            return JsonResponse({
                "error": "POST request required."
            }, status=400)                   