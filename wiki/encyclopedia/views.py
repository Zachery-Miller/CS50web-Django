from http.client import HTTPResponse
from django.shortcuts import render, HttpResponse, redirect
from random import randint
from django import forms

from . import util
import encyclopedia
import markdown2

class NewPageForm(forms.Form):
    # title field
    title = forms.CharField(label="Entry Title", max_length=100)

    # textarea field
    entry_content = forms.CharField(widget=forms.Textarea, label="Entry Markdown Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["entry_content"]
            util.save_entry(title, content)

            entry = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                "content": entry, "title": title
            })

        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })

    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def randompage(request):
    # pull random entry from entries and convert markdown to HTML
    entries = util.list_entries()
    title = entries[randint(0, len(entries) - 1)]
    entry = markdown2.markdown(util.get_entry(title))
    return render(request, "encyclopedia/entry.html", {
        "content": entry, "title": title
    })

def display_markdown(request, title):
    # see if entry exists
    try:
        entry = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "content": entry, "title": title
        })
    
    # redirect to index if page does not exist when accessed via hardcoded URL
    except TypeError:
        return redirect('index')

def search(request):
    if request.method == "POST":
        # get query from POST
        title = request.POST.get('q')

        # get encylcopedia entries
        entries = util.list_entries()

        # initialize search results list
        search_results = []
        
        # check if exact entry exists by search and render page if so
        for entry in entries:
            if title.lower() == entry.lower():
                searched_entry = markdown2.markdown(util.get_entry(title))
                return render(request, "encyclopedia/entry.html", {
                    "content": searched_entry, "title": title
                })
            
            # checks if search is a substring of existing entry. if so, entry is add to search_results list
            elif entry.lower().find(title.lower()) != -1:
                search_results.append(entry)

            # continue looping if above conditions are not met
            else:
                continue
        
        # if entry is not found, return all results where search matches a substring of an existing entry
        return render(request, "encyclopedia/results.html", {
            "results": search_results
        })

    # redirect to index if accessed via GET / absolute URL
    else:
        return redirect('index')


def edit(request):
    if request.method == "POST":
        return HttpResponse("Edit GET!")

    # redirect to index if accessed via GET / absolute URL
    else:
        return redirect('index')