from django.urls import path

from . import views

app_name="wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:page>/", views.getwiki, name="getwiki"),
    path("search", views.search, name="search"),
    path("newpage", views.newpage, name="newpage"),    
    path("editpage/<str:page>", views.editpage, name="editpage"),  
    path("random", views.random, name="random")
]