from django.shortcuts import render
from random import randint

from . import util
import encyclopedia
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newpage(request):
    return render(request, "encyclopedia/newpage.html")

def randompage(request):
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    entry = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "content": entry, "title": title
    })

def display_markdown(request, title):
    entry = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "content": entry, "title": title
    })