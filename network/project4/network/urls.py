
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),

    # API Routes
    path("posts", views.posts, name="posts"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("profile/<str:user_profile>", views.profile, name="profile"),
    path("follow/<str:user_profile>", views.follow, name="follow"),
    path("like/<str:post_id>", views.like, name="like"),
    path("edit_post/<str:post_id>", views.edit_post, name="edit_post"),
]
