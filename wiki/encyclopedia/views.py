import random
from django.shortcuts import render, redirect
import markdown

from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content is None:
        return render(request, "encyclopedia/error.html", {
            "message": "This entry does not exist"
        })
    else:
        content_html = markdown.markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": content_html
        })

def search(request):
    query = request.GET.get('q', '')
    entries = util.list_entries()
    matching_entries = [entry for entry in entries if query.lower() in entry.lower()]
    if len(matching_entries) == 1 and matching_entries[0].lower() == query.lower():
        return entry(request, matching_entries[0])
    else:
        return render(request, "encyclopedia/search.html", {
            "query": query,
            "entries": matching_entries
        })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry already exists"
            })
        else:
            content = "# " + title + "\n\n" + content
            util.save_entry(title, content)
            return entry(request, title)
    else:
        return render(request, "encyclopedia/new_page.html")
    
    
def edit_page(request, title):
    if request.method == "POST":
        content = request.POST.get('content')
        util.save_entry(title, content)
        return redirect("entry", title=title)
    else:
        content = util.get_entry(title)
        if content is None:
            return render(request, "encyclopedia/error.html", {
                "message": "This entry does not exist"
            })
        return render(request, "encyclopedia/edit_page.html", {
            "title": title,
            "content": content
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect("entry", title=random_entry)