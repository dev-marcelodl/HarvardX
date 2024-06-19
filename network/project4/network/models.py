from django.contrib.auth.models import AbstractUser
from django.db import models

url_empty = "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/Image_not_available.png/640px-Image_not_available.png"

class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    age = models.IntegerField()
    gender = models.CharField(max_length=1)
    picture =  models.URLField(max_length=255, blank=True, null=True, default="")
    followers = models.ManyToManyField(User, blank=True, related_name="users_followers")

    def serialize(self):

        #count following
        user = User.objects.filter(username=self.user.username)
        count_following = Profile.objects.filter(followers__in=user).count()

        v_picture = ""
        if self.picture == "" or self.picture == None:
           v_picture = url_empty
        else: 
           v_picture = self.picture

        return {
            "username": self.user.username,
            "age": self.age,
            "gender": self.gender,
            "picture": v_picture,
            "followers": [user.username for user in self.followers.all()],
            "count_followers" : self.followers.all().count(),   
            "count_following" : count_following   
        }


class Post(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.CharField (max_length=4000)    
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name="users_posts")   
    likes = models.ManyToManyField(User, blank=True, related_name="users_likes")

    def serialize(self):

        v_picture = Profile.objects.filter(user=self.user)[0].picture

        if v_picture == "" or v_picture == None:
           v_picture = url_empty

        return {
            "id": self.id,
            "content": self.content,
            "username": self.user.username,
            "created": self.created.strftime("%b %d %Y, %I:%M %p"),
            "likes_list": ','.join([user.username for user in self.likes.all()]),
            "likes": [user.username for user in self.likes.all()],
            "count_likes" : self.likes.all().count(),
            "picture" :  v_picture
        }
