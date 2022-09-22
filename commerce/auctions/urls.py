from django.urls import path

from . import views

app_name = 'auctions'
urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.create_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:category>", views.category_search, name="category_search"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("<int:listing_id>/new_bid", views.new_bid, name="new_bid"),
    path("<int:listing_id>/new_comment", views.new_comment, name="new_comment"),
    path("<int:listing_id>/watchlist_add", views.add_to_watchlist, name="add_to_watchlist"),
    path("<int:listing_id>/watchlist_remove", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("<int:listing_id>/close_listing", views.close_listing, name="close_listing")
]
