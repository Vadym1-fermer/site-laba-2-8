from django.test import TestCase
from django.urls import reverse

from .admin import ClothingCategoryAdmin, OrderAdmin, ProductAdmin
from .models import ClothingCategory, Order, Product


class PagesTests(TestCase):
    def test_home_page_has_links_to_other_pages(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")
        self.assertContains(response, "Contacts")
        self.assertContains(response, reverse("pages:about"))
        self.assertContains(response, reverse("pages:contacts"))

    def test_inner_pages_have_link_to_home(self):
        for page_name in ("pages:about", "pages:contacts"):
            response = self.client.get(reverse(page_name))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, reverse("pages:home"))


class ModelTests(TestCase):
    def test_product_and_order_are_linked_to_parent_tables(self):
        category = ClothingCategory.objects.create(
            name="T-shirts",
            description="Casual clothing",
        )
        product = Product.objects.create(
            category=category,
            name="White T-shirt",
            size="M",
            color="White",
            price="499.00",
        )
        order = Order.objects.create(
            product=product,
            customer_name="Vadim",
            quantity=2,
            phone="+380000000000",
        )

        self.assertEqual(str(category), "T-shirts")
        self.assertEqual(str(product), "White T-shirt")
        self.assertEqual(order.product.category, category)


class AdminTests(TestCase):
    def test_admin_tables_show_required_columns(self):
        self.assertEqual(
            ClothingCategoryAdmin.list_display,
            ("name", "created_at", "updated_at"),
        )
        self.assertEqual(
            ProductAdmin.list_display,
            ("name", "category", "size", "color", "price", "created_at", "updated_at"),
        )
        self.assertEqual(
            OrderAdmin.list_display,
            ("customer_name", "product", "quantity", "phone", "created_at", "updated_at"),
        )
