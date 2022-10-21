
from django.urls import path

from . import views

urlpatterns = [
    path("explore", views.explore, name="explore"),
    path("home", views.home, name="home"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:profile_user_username>", views.profile_page, name="profile"),
    path("profile/<str:profile_user_username>/follow", views.follow, name="follow"),
    path("profile/<str:profile_user_username>/unfollow", views.unfollow, name="unfollow"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("delete_post/<int:post_id>", views.delete_post, name="delete_post"),
    
    # api
    path("check_follow/<str:profile_user>", views.check_follow_status, name="check_follow"),
    path("toggle_like/<int:post_id>", views.toggle_like, name="toggle_like")
]
