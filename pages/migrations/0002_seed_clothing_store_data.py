from django.db import migrations


def seed_data(apps, schema_editor):
    ClothingCategory = apps.get_model("pages", "ClothingCategory")
    Product = apps.get_model("pages", "Product")
    Order = apps.get_model("pages", "Order")

    tshirts, _ = ClothingCategory.objects.get_or_create(
        name="T-shirts",
        defaults={"description": "Casual cotton T-shirts for everyday outfits."},
    )
    jeans, _ = ClothingCategory.objects.get_or_create(
        name="Jeans",
        defaults={"description": "Denim clothing for daily wear."},
    )
    hoodies, _ = ClothingCategory.objects.get_or_create(
        name="Hoodies",
        defaults={"description": "Warm hoodies for cooler days."},
    )

    white_tshirt, _ = Product.objects.get_or_create(
        name="White T-shirt",
        defaults={
            "category": tshirts,
            "size": "M",
            "color": "White",
            "price": "499.00",
            "description": "Basic white cotton T-shirt.",
        },
    )
    blue_jeans, _ = Product.objects.get_or_create(
        name="Blue Jeans",
        defaults={
            "category": jeans,
            "size": "32",
            "color": "Blue",
            "price": "1299.00",
            "description": "Classic straight fit blue jeans.",
        },
    )
    black_hoodie, _ = Product.objects.get_or_create(
        name="Black Hoodie",
        defaults={
            "category": hoodies,
            "size": "L",
            "color": "Black",
            "price": "1599.00",
            "description": "Soft hoodie with a minimal dark look.",
        },
    )

    Order.objects.get_or_create(
        product=white_tshirt,
        customer_name="Vadim",
        defaults={"quantity": 2, "phone": "+380000000000"},
    )
    Order.objects.get_or_create(
        product=blue_jeans,
        customer_name="Student",
        defaults={"quantity": 1, "phone": "+380111111111"},
    )
    Order.objects.get_or_create(
        product=black_hoodie,
        customer_name="Customer",
        defaults={"quantity": 1, "phone": "+380222222222"},
    )


def remove_seed_data(apps, schema_editor):
    ClothingCategory = apps.get_model("pages", "ClothingCategory")
    ClothingCategory.objects.filter(name__in=["T-shirts", "Jeans", "Hoodies"]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_data, remove_seed_data),
    ]
