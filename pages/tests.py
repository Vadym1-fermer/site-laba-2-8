from django.test import TestCase
from django.urls import reverse

from .admin import (
    ClothingCategoryAdmin,
    NewsletterSubscriberAdmin,
    OrderAdmin,
    ProductAdmin,
    ProductRatingAdmin,
)
from .models import ClothingCategory, NewsletterSubscriber, Order, Product, ProductRating


class PagesTests(TestCase):
    def setUp(self):
        self.category = ClothingCategory.objects.create(
            name="T-shirts",
            description="Casual clothing",
        )
        self.other_category = ClothingCategory.objects.create(
            name="Jeans",
            description="Denim clothing",
        )
        self.product = Product.objects.create(
            category=self.category,
            name="White T-shirt",
            size="M",
            color="White",
            price="499.00",
            image_url="https://example.com/tshirt.jpg",
            description="Basic cotton T-shirt",
        )
        Product.objects.create(
            category=self.other_category,
            name="Blue Jeans",
            size="32",
            color="Blue",
            price="1299.00",
            image_url="https://example.com/jeans.jpg",
            description="Classic jeans",
        )
        Product.objects.create(
            category=self.category,
            name="Black T-shirt",
            size="L",
            color="Black",
            price="549.00",
            image_url="https://example.com/black-tshirt.jpg",
            description="Minimal black cotton T-shirt",
        )
        Product.objects.create(
            category=self.category,
            name="Oversized T-shirt",
            size="XL",
            color="Gray",
            price="599.00",
            image_url="https://example.com/oversized-tshirt.jpg",
            description="Loose gray T-shirt",
        )

    def test_home_page_has_links_to_other_pages(self):
        response = self.client.get(reverse("pages:home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "About")
        self.assertContains(response, "Contacts")
        self.assertContains(response, reverse("pages:about"))
        self.assertContains(response, reverse("pages:contacts"))
        self.assertContains(response, "Clothing Store")
        self.assertContains(response, "White T-shirt")
        self.assertContains(response, "Blue Jeans")
        self.assertContains(response, "All products")
        self.assertContains(response, "View product")

    def test_inner_pages_have_link_to_home(self):
        for page_name in ("pages:about", "pages:contacts"):
            response = self.client.get(reverse(page_name))

            self.assertEqual(response.status_code, 200)
            self.assertContains(response, reverse("pages:home"))

    def test_category_page_has_only_products_from_selected_category(self):
        response = self.client.get(reverse("pages:category_detail", args=[self.category.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "White T-shirt")
        self.assertContains(response, "Black T-shirt")
        self.assertContains(response, "Oversized T-shirt")
        self.assertNotContains(response, "Blue Jeans")

    def test_product_page_has_photo_price_and_buy_button(self):
        response = self.client.get(reverse("pages:product_detail", args=[self.product.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "https://example.com/tshirt.jpg")
        self.assertContains(response, "499.00 UAH")
        self.assertContains(response, "Add to cart")
        self.assertContains(response, "Rate this product")
        self.assertContains(response, reverse("pages:home"))

    def test_product_rating_is_saved_and_average_is_shown(self):
        response = self.client.post(
            reverse("pages:product_detail", args=[self.product.id]),
            {
                "user_name": "Vadim",
                "score": 5,
                "comment": "Good quality",
                "rating_submit": "1",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ProductRating.objects.count(), 1)
        self.assertContains(response, "5.0 / 5")

    def test_product_can_be_added_to_cart(self):
        response = self.client.post(
            reverse("pages:product_detail", args=[self.product.id]),
            {"add_to_cart": "1"},
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cart")
        self.assertContains(response, "White T-shirt")
        self.assertContains(response, "499.00 UAH")

    def test_newsletter_signup_saves_email(self):
        response = self.client.post(
            reverse("pages:newsletter_signup"),
            {
                "name": "Vadim",
                "email": "vadim@example.com",
                "next": reverse("pages:home"),
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(NewsletterSubscriber.objects.filter(email="vadim@example.com").exists())


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
            image_url="https://example.com/tshirt.jpg",
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
        self.assertEqual(
            NewsletterSubscriberAdmin.list_display,
            ("email", "name", "created_at", "updated_at"),
        )
        self.assertEqual(
            ProductRatingAdmin.list_display,
            ("product", "user_name", "score", "created_at", "updated_at"),
        )
