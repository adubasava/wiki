from django.shortcuts import render
import markdown2
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


# Convert Markdown to HTML using markdown2 library
def md_to_html(title):
    if util.get_entry(title):
        return markdown2.markdown(util.get_entry(title))
        

# Displays encyclopedia entry if entry exists
# otherwise renders error page
def entry(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": md_to_html(title)
        })
    else:
        return render(request, "encyclopedia/error.html")
    

# Search for an entry
# if there is no full match, displays all partial matches
def search(request):
    if request.method == "POST":
        if util.get_entry(request.POST['q']):
            return render(request, "encyclopedia/entry.html", {
                "title": request.POST['q'],
                "content": md_to_html(request.POST['q'])
            })
        else:
            list = []
            for item in util.list_entries():
                if request.POST['q'].lower() in item.lower():
                    list.append(item)
            return render(request, "encyclopedia/search.html", {
                "list": list
            })
        

# Displays random page
def random_page(request):
    title = random.choice(util.list_entries())
    return entry(request, title)


# Allows a user to create a new page (and redirects to it)
# if an entry already exists, shows an error message
def create(request):
    if request.method == "GET":
        return render(request, "encyclopedia/create.html")
    if request.method == "POST":
        if request.POST['title'] not in util.list_entries():
            util.save_entry(request.POST['title'], request.POST['content'])
            return entry(request, request.POST['title'])
        else:
            return render(request, "encyclopedia/create.html", {
                "error": "An entry already exists!"
            })


# Allows a user to edit any page
def edit(request):
    if request.method == "POST":
        return render(request, "encyclopedia/edit.html", {
            "title": request.POST['title'],
            "content": util.get_entry(request.POST['title'])
        })
    

# After saving an edited entry, redirects a user to that entry
def save(request):
    if request.method == "POST":
        util.save_entry(request.POST['title'], request.POST['content'])
        return entry(request, request.POST['title'])