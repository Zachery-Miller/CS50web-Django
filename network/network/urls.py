
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<str:user>", views.profile_page, name="profile"),
    path("profile/<str:user>/toggle_follow", views.toggle_follow, name="toggle_follow"),

    # API Routes // Validate access to these routes can only be performed via POST
    path("check_following/<str:user>", views.check_following, name="check_following"),
    #path("toggle_like/<int:post_id>, views.toggle_like, name=toggle_like"),
    path("new_post", views.new_post, name="new_post"),
    path("show_posts/<str:page>", views.show_posts, name="show_posts")
]
