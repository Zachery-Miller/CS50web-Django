
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile_page, name="profile"),

    # API Routes // Validate access to these routes can only be performed via POST
    path("toggle_follow/<str:user>", views.toggle_follow, name="toggle_follow"),
    #path("toggle_like/<int:post_id>, views.toggle_like, name=toggle_like"),
    path("new_post", views.new_post, name="new_post"),
    path("show_posts/<str:page>", views.show_posts, name="show_posts")
]
