from django.urls import path

from . import views

# place display markdown url on bottom of url patterns list otherwise it interferes with other links given its design
urlpatterns = [
    path("", views.index, name="index"),
    path("newpage/", views.newpage, name="newpage"),
    path("randompage/", views.randompage, name="randompage"),
    path("searchresults/", views.search, name="search"),
    path("edit/", views.edit, name="edit"),
    path("<str:title>/", views.display_markdown, name="display_markdown")
]
