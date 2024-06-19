from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("closed_index", views.closed_index, name="closed_index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:auction_id>/", views.listing, name="listing"),
    path("add_watchlist/<str:auction_id>/", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist/<str:auction_id>/", views.remove_watchlist, name="remove_watchlist"),
    path("bid_item/<str:auction_id>/", views.bid_item, name="bid_item"),
    path("auction_close/<str:auction_id>/", views.auction_close, name="auction_close"),
    path("comment_auction/<str:auction_id>/", views.comment_auction, name="comment_auction"),
    path("my_watchlist", views.my_watchlist, name="my_watchlist"),   
    path("categories", views.categories, name="categories"),
    path("category_listing/<str:category_name>/", views.category_listing, name="category_listing"),  
       
]
