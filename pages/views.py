from django.shortcuts import render

from .models import ClothingCategory, Product


PAGES = [
    {
        "title": "About",
        "description": "Information about our clothing store.",
        "url_name": "about",
    },
    {
        "title": "Contacts",
        "description": "Contact details for customer support.",
        "url_name": "contacts",
    },
]


def get_site_context():
    return {
        "pages": PAGES,
        "categories": ClothingCategory.objects.all(),
    }


def home(request):
    selected_category_id = request.GET.get("category")
    products = Product.objects.select_related("category")

    if selected_category_id:
        products = products.filter(category_id=selected_category_id)

    context = {
        **get_site_context(),
        "title": "Clothing Store",
        "products": products,
        "selected_category_id": selected_category_id,
    }
    return render(request, "pages/home.html", context)


def about(request):
    context = {
        **get_site_context(),
        "title": "About",
        "content": "Our store offers comfortable everyday clothing with simple ordering and clear categories.",
    }
    return render(request, "pages/page.html", context)


def contacts(request):
    context = {
        **get_site_context(),
        "title": "Contacts",
        "content": "Contact us to ask about sizes, colors, availability, and delivery.",
    }
    return render(request, "pages/page.html", context)
