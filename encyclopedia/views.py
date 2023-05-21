from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "error": "Page not found.",
        })

    markdown = Markdown()
    html = markdown.convert(content)

    return render(request, "encyclopedia/entry.html", {
        "title": title.capitalize(),
        "content": html,
    })


def search(request):
    query = request.POST.get('q', '')

    entries = util.list_entries()
    results = []
    if query != "":
        for entry in entries:
            if query.lower() == entry.lower():
                return HttpResponseRedirect(reverse("entry", args=(query,)))
            elif query.lower() in entry.lower():
                results.append(entry)

    return render(request, "encyclopedia/search.html", {
        "results": results,
        "query": query,
    })

def createNewPage(request):
    if request.method == "GET":
        return render(request, "encyclopedia/createNewPage.html")
    
    title = request.POST.get('title', '')
    content = request.POST.get('content', '')

    if title == "":
        return render(request, "encyclopedia/createNewPage.html", {
            "error": "Title can not be empty.",
            "title": title,
            "content": content,
        })
    
    for entry in util.list_entries():
        if title.lower() == entry.lower():
            return render(request, "encyclopedia/createNewPage.html", {
                "error": "Page already exists.",
                "title": title,
                "content": content,
            })
    
    if content == "":
        return render(request, "encyclopedia/createNewPage.html", {
            "error": "Content can not be empty.",
            "title": title,
            "content": content,
        })

    util.save_entry(title, content)

    return HttpResponseRedirect(reverse('entry', args=(title,)))
    

def editPage(request, title):
    if request.method == "GET":
        content = util.get_entry(title)
        return render(request, "encyclopedia/editPage.html", {
            "title": title,
            "content": content,
        })
    
    content = request.POST.get('content', '')
    util.save_entry(title, content)

    return HttpResponseRedirect(reverse('entry', args=(title,)))

def randomPage(request):
    entries = util.list_entries()
    return HttpResponseRedirect(reverse('entry', args=(choice(entries),)))