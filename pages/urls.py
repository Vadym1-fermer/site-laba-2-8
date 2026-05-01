from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("products/<int:pk>/add-to-cart/", views.add_to_cart, name="add_to_cart"),
    path("cart/", views.cart, name="cart"),
    path("newsletter/", views.newsletter_signup, name="newsletter_signup"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
]
