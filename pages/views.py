from django.shortcuts import render


PAGES = [
    {
        "title": "About",
        "description": "Information page created for lab 3.",
        "url_name": "about",
    },
    {
        "title": "Contacts",
        "description": "Contacts page created for lab 3.",
        "url_name": "contacts",
    },
]


def home(request):
    context = {
        "title": "Home",
        "pages": PAGES,
    }
    return render(request, "pages/home.html", context)


def about(request):
    context = {
        "title": "About",
        "content": "This page is rendered with a Django template and context.",
    }
    return render(request, "pages/page.html", context)


def contacts(request):
    context = {
        "title": "Contacts",
        "content": "This contacts page also receives its content from context.",
    }
    return render(request, "pages/page.html", context)
