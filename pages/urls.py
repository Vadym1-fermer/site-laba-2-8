from django.urls import path

from . import views

app_name = "pages"

urlpatterns = [
    path("", views.home, name="home"),
    path("categories/<int:pk>/", views.category_detail, name="category_detail"),
    path("products/<int:pk>/", views.product_detail, name="product_detail"),
    path("about/", views.about, name="about"),
    path("contacts/", views.contacts, name="contacts"),
]
