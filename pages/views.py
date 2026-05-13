import random
from datetime import timedelta

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import (
    NewsletterSubscriberForm,
    PasswordResetConfirmForm,
    PasswordResetRequestForm,
    ProductRatingForm,
    RegisterForm,
)
from .models import ClothingCategory, NewsletterSubscriber, Order, PasswordResetCode, Product


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


@login_required
def checkout(request):
    cart_data = get_cart(request)
    if not cart_data:
        messages.error(request, "Your cart is empty.")
        return redirect("pages:cart")

    products = Product.objects.filter(id__in=cart_data.keys())
    for product in products:
        Order.objects.create(
            user=request.user,
            product=product,
            customer_name=request.user.get_username(),
            quantity=cart_data.get(str(product.id), 1),
            phone="Not provided",
        )

    request.session["cart"] = {}
    request.session.modified = True
    messages.success(request, "Order created successfully.")
    return redirect("pages:account")


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


def login_view(request):
    if request.user.is_authenticated:
        return redirect("pages:account")

    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("pages:account")

    return render(
        request,
        "pages/auth_form.html",
        {
            **site_context(request),
            "title": "Login",
            "form": form,
            "button_text": "Login",
        },
    )


def logout_view(request):
    logout(request)
    return redirect("pages:home")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("pages:account")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save(commit=False)
        user.email = form.cleaned_data["email"]
        user.save()
        login(request, user)
        messages.success(request, "Registration completed.")
        return redirect("pages:account")

    return render(
        request,
        "pages/auth_form.html",
        {
            **site_context(request),
            "title": "Register",
            "form": form,
            "button_text": "Register",
        },
    )


@login_required
def account(request):
    if request.user.is_staff:
        orders = Order.objects.select_related("product", "user").all()
    else:
        orders = Order.objects.select_related("product").filter(user=request.user)

    return render(
        request,
        "pages/account.html",
        {
            **site_context(request),
            "title": "Account",
            "orders": orders,
        },
    )


def password_reset_request(request):
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"]
        user = User.objects.filter(email=email).first()
        if user:
            code = f"{random.randint(100000, 999999)}"
            PasswordResetCode.objects.create(
                user=user,
                code=code,
                expires_at=timezone.now() + timedelta(minutes=15),
            )
            send_mail(
                "Password reset code",
                f"Your temporary password reset code is: {code}",
                None,
                [email],
                fail_silently=False,
            )
        messages.success(request, "If this email exists, a reset code has been sent.")
        return redirect("pages:password_reset_confirm")

    return render(
        request,
        "pages/auth_form.html",
        {
            **site_context(request),
            "title": "Reset password",
            "form": form,
            "button_text": "Send code",
        },
    )


def password_reset_confirm(request):
    form = PasswordResetConfirmForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = User.objects.filter(email=form.cleaned_data["email"]).first()
        reset_code = None
        if user:
            reset_code = PasswordResetCode.objects.filter(
                user=user,
                code=form.cleaned_data["code"],
            ).first()

        if reset_code and reset_code.is_valid():
            user.set_password(form.cleaned_data["new_password"])
            user.save()
            reset_code.used = True
            reset_code.save()
            messages.success(request, "Password changed. You can log in now.")
            return redirect("pages:login")

        messages.error(request, "Invalid or expired reset code.")

    return render(
        request,
        "pages/auth_form.html",
        {
            **site_context(request),
            "title": "Enter reset code",
            "form": form,
            "button_text": "Change password",
        },
    )
