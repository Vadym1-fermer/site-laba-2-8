from django.contrib import admin
from .models import (
    ClothingCategory,
    NewsletterSubscriber,
    Order,
    PasswordResetCode,
    Product,
    ProductRating,
)


@admin.register(ClothingCategory)
class ClothingCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "size", "color", "price", "created_at", "updated_at")
    list_filter = ("category",)
    search_fields = ("name", "description", "color")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("customer_name", "user", "product", "quantity", "phone", "created_at", "updated_at")
    list_filter = ("product", "user")
    search_fields = ("customer_name", "phone", "user__username")


@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "created_at", "updated_at")
    search_fields = ("email", "name")


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ("product", "user_name", "score", "created_at", "updated_at")
    list_filter = ("product", "score")
    search_fields = ("product__name", "user_name", "comment")


@admin.register(PasswordResetCode)
class PasswordResetCodeAdmin(admin.ModelAdmin):
    list_display = ("user", "code", "expires_at", "used", "created_at")
    list_filter = ("used", "expires_at")
    search_fields = ("user__username", "user__email", "code")
