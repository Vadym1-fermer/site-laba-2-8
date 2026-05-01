from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render

from .forms import NewsletterSubscriberForm, ProductRatingForm
from .models import ClothingCategory, NewsletterSubscriber, Product


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


def get_cart(request):
    return request.session.setdefault("cart", {})


def get_cart_count(request):
    return sum(get_cart(request).values())


def site_context(request):
    return {
        "pages": PAGES,
        "categories": ClothingCategory.objects.all(),
        "cart_count": get_cart_count(request),
        "newsletter_form": NewsletterSubscriberForm(),
    }


def home(request):
    products = Product.objects.select_related("category")

    context = {
        **site_context(request),
        "title": "Clothing Store",
        "products": products,
    }
    return render(request, "pages/home.html", context)


def category_detail(request, pk):
    category = get_object_or_404(ClothingCategory, pk=pk)
    context = {
        **site_context(request),
        "title": category.name,
        "category": category,
        "products": category.products.all(),
    }
    return render(request, "pages/category_detail.html", context)


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related("category"), pk=pk)
    rating_form = ProductRatingForm()

    if request.method == "POST":
        if "rating_submit" in request.POST:
            rating_form = ProductRatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.product = product
                rating.save()
                messages.success(request, "Your rating has been saved.")
                return redirect("pages:product_detail", pk=product.pk)

        if "add_to_cart" in request.POST:
            cart = get_cart(request)
            product_id = str(product.pk)
            cart[product_id] = cart.get(product_id, 0) + 1
            request.session.modified = True
            messages.success(request, "Product added to cart.")
            return redirect("pages:cart")

    rating_summary = product.ratings.aggregate(average=Avg("score"))
    context = {
        **site_context(request),
        "title": product.name,
        "product": product,
        "rating_form": rating_form,
        "average_rating": rating_summary["average"],
        "ratings": product.ratings.all(),
    }
    return render(request, "pages/product_detail.html", context)


def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart = get_cart(request)
    product_id = str(product.pk)
    cart[product_id] = cart.get(product_id, 0) + 1
    request.session.modified = True
    messages.success(request, "Product added to cart.")
    return redirect("pages:cart")


def cart(request):
    cart_data = get_cart(request)
    products = Product.objects.filter(id__in=cart_data.keys()).select_related("category")
    cart_items = []
    total = 0

    for product in products:
        quantity = cart_data.get(str(product.id), 0)
        subtotal = product.price * quantity
        cart_items.append(
            {
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            }
        )
        total += subtotal

    context = {
        **site_context(request),
        "title": "Cart",
        "cart_items": cart_items,
        "total": total,
    }
    return render(request, "pages/cart.html", context)


def newsletter_signup(request):
    if request.method != "POST":
        return redirect("pages:home")

    form = NewsletterSubscriberForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data["email"]
        subscriber, created = NewsletterSubscriber.objects.get_or_create(
            email=email,
            defaults={"name": form.cleaned_data["name"]},
        )
        if not created and form.cleaned_data["name"]:
            subscriber.name = form.cleaned_data["name"]
            subscriber.save()
        messages.success(request, "You are subscribed to the newsletter.")
    else:
        messages.error(request, "Please enter a valid email for newsletter signup.")

    return redirect(request.POST.get("next") or "pages:home")


def about(request):
    context = {
        **site_context(request),
        "title": "About",
        "content": "Our store offers comfortable everyday clothing with simple ordering and clear categories.",
    }
    return render(request, "pages/page.html", context)


def contacts(request):
    context = {
        **site_context(request),
        "title": "Contacts",
        "content": "Contact us to ask about sizes, colors, availability, and delivery.",
    }
    return render(request, "pages/page.html", context)
