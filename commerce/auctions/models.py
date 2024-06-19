from email.policy import default
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField (primary_key=True, max_length=50)  

    def __str__(self):
	    return self.name

class Auction(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField (max_length=50)
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, null=True, default="", related_name="categories")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(max_length=255, blank=True, null=True, default="")
    created = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="users_auctions")
    watchlist = models.ManyToManyField(User, blank=True, related_name="users_watch")
    enabled = models.BooleanField(default=True)

    def __str__(self):
	    return self.title

class Comment(models.Model):
    post_id = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments_auctions")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    comment =  models.CharField(max_length=255)
    created = models.DateField()

    def __str__(self):
	     return f"{self.auction_id} - {self.user} - {self.comment}" 

class Followers(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following_user")
    user_follower  = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower_user")    
    created = models.DateField()

    def __str__(self):
	    return f"{self.user_following} - {self.user_follower}" 

