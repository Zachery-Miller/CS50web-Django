from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newpage(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def randompage(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })