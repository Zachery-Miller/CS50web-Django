from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.newpage, name="newpage"),
    path("randompage/", views.randompage, name="randompage"),
    path("<str:title>/", views.display_markdown, name="display_markdown")
]
