import datetime
from decimal import Decimal
from sqlite3 import enable_shared_cache
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.db.models import Max

from auctions.forms import AuctionForm

from .models import Auction, Category, Comment, User, Bid


def index(request):
    user_logged = request.user
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(enabled=True)
    })

def closed_index(request):
    user_logged = request.user
   
    lst = []
    auctions_disableds = Auction.objects.filter(enabled=False)
    for auction in auctions_disableds:
        bid = Bid.objects.filter(auction_id=auction.id).latest('bid')
        if (bid != None):
            if (bid.user == user_logged):
                lst.append(bid.auction_id.id)

    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(enabled=False, id__in=lst)
    })

def my_watchlist(request):
    user_logged = request.user
    user = User.objects.filter(username=user_logged)

    auctions = Auction.objects.filter(watchlist__in=user)
    return render(request, "auctions/index.html", {
        "auctions":  auctions
    })

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.filter()
    })   

def category_listing(request, category_name):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.filter(category=category_name)
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

def create(request):
        if request.method == "POST":
            form = AuctionForm(request.POST)
            if form.is_valid():
               auction = form.save(commit=False)
               auction.user = request.user 
               auction.created = datetime.datetime.now()
               auction.views = 0
               auction.save()
                                      
            return HttpResponseRedirect(reverse("index"))
            
        auction_form = AuctionForm()
        auction = Auction.objects.all()
        return render(request=request, template_name="auctions/create.html", context={'auction_form':auction_form, 'auction':auction})    

    
def listing(request, auction_id):
    try:
        user_logged = request.user
        is_watchlist = False

        auction = Auction.objects.get(id=auction_id)
        auction.views = auction.views + 1 
        auction.save()

        bids = Bid.objects.filter(auction_id=auction_id)
        bid = bids.aggregate(Max('bid'))
        max_bid = bid['bid__max']
        if (max_bid == None):
            max_bid =  0        

        if (max_bid == 0):
            min_bid = Decimal(auction.price) + Decimal(0.01)
        else:
            min_bid = Decimal(max_bid) + Decimal(0.01)

        print(min_bid)

        if auction.watchlist.all().filter(username=user_logged):
           is_watchlist = True

        users_watch = auction.watchlist.all()

        comment_auction = Comment.objects.filter(auction_id=auction_id)


    except Auction.DoesNotExist:
        raise Http404("Auction not found.")
    return render(request, "auctions/listing.html", {
        "auction": auction, "min_bid": min_bid, "max_bid": max_bid, "is_watchlist": is_watchlist, "users_watch" : users_watch, "comments": comment_auction
    })

def add_watchlist(request, auction_id):

        if request.method == "POST":
            user_logged = request.user
            auction = Auction.objects.get(id=auction_id)
            auction.watchlist.add(user_logged)
            auction.save()            
            
        return  listing(request, auction_id);     

        
def remove_watchlist(request, auction_id):

        if request.method == "POST":
            user_logged = request.user
            auction = Auction.objects.get(id=auction_id)
            auction.watchlist.remove(user_logged)
            auction.save()

        return  listing(request, auction_id);  


def bid_item(request, auction_id):

        if request.method == "POST":

            bid_value = request.POST.get('bid_value')
            user_logged = request.user
            bid = Bid()
            bid.auction_id=Auction.objects.get(id=auction_id)
            bid.user=user_logged
            bid.bid=bid_value

            bid.created=datetime.datetime.now() 
            bid.save()
                             
        return  listing(request, auction_id);     

def auction_close(request, auction_id):

        if request.method == "POST":
            auction = Auction.objects.get(id=auction_id)
            auction.enabled = False
            auction.save() 
            return HttpResponseRedirect(reverse("index"))           
            
        return  listing(request, auction_id);    

def comment_auction(request, auction_id):

        if request.method == "POST":

            comment_value = request.POST.get('comment_value')
            user_logged = request.user
            comment = Comment()
            comment.auction_id=Auction.objects.get(id=auction_id)
            comment.user=user_logged
            comment.comment=comment_value
            comment.created=datetime.datetime.now() 
            comment.save()
                             
        return  listing(request, auction_id);      
