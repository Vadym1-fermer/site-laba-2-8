from django.shortcuts import get_object_or_404, render

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
    products = Product.objects.select_related("category")

    context = {
        **get_site_context(),
        "title": "Clothing Store",
        "products": products,
    }
    return render(request, "pages/home.html", context)


def category_detail(request, pk):
    category = get_object_or_404(ClothingCategory, pk=pk)
    context = {
        **get_site_context(),
        "title": category.name,
        "category": category,
        "products": category.products.all(),
    }
    return render(request, "pages/category_detail.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    context = {
        **get_site_context(),
        "title": product.name,
        "product": product,
    }
    return render(request, "pages/product_detail.html", context)


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
