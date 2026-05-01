from django.db import migrations


MORE_PRODUCTS = [
    {
        "category": "T-shirts",
        "name": "Black T-shirt",
        "size": "L",
        "color": "Black",
        "price": "549.00",
        "description": "Minimal black cotton T-shirt for everyday outfits.",
        "image_url": "https://images.unsplash.com/photo-1503341504253-dff4815485f1?auto=format&fit=crop&w=900&q=80",
    },
    {
        "category": "Jeans",
        "name": "Black Jeans",
        "size": "34",
        "color": "Black",
        "price": "1399.00",
        "description": "Dark denim jeans with a clean casual look.",
        "image_url": "https://images.unsplash.com/photo-1511196044526-5cb3bcb7071b?auto=format&fit=crop&w=900&q=80",
    },
    {
        "category": "Hoodies",
        "name": "Beige Hoodie",
        "size": "M",
        "color": "Beige",
        "price": "1499.00",
        "description": "Comfortable beige hoodie for relaxed daily wear.",
        "image_url": "https://images.unsplash.com/photo-1578587018452-892bacefd3f2?auto=format&fit=crop&w=900&q=80",
    },
]


def add_more_products(apps, schema_editor):
    ClothingCategory = apps.get_model("pages", "ClothingCategory")
    Product = apps.get_model("pages", "Product")

    for item in MORE_PRODUCTS:
        category = ClothingCategory.objects.get(name=item["category"])
        Product.objects.get_or_create(
            name=item["name"],
            defaults={
                "category": category,
                "size": item["size"],
                "color": item["color"],
                "price": item["price"],
                "description": item["description"],
                "image_url": item["image_url"],
            },
        )


def remove_more_products(apps, schema_editor):
    Product = apps.get_model("pages", "Product")
    Product.objects.filter(name__in=[item["name"] for item in MORE_PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_product_image_url"),
    ]

    operations = [
        migrations.RunPython(add_more_products, remove_more_products),
    ]
