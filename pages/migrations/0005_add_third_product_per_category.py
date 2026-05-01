from django.db import migrations


THIRD_PRODUCTS = [
    {
        "category": "T-shirts",
        "name": "Oversized T-shirt",
        "size": "XL",
        "color": "Gray",
        "price": "599.00",
        "description": "Loose gray T-shirt for a relaxed streetwear look.",
        "image_url": "https://images.unsplash.com/photo-1562157873-818bc0726f68?auto=format&fit=crop&w=900&q=80",
    },
    {
        "category": "Jeans",
        "name": "Light Blue Jeans",
        "size": "30",
        "color": "Light blue",
        "price": "1199.00",
        "description": "Light denim jeans for casual everyday outfits.",
        "image_url": "https://images.unsplash.com/photo-1475178626620-a4d074967452?auto=format&fit=crop&w=900&q=80",
    },
    {
        "category": "Hoodies",
        "name": "Green Hoodie",
        "size": "M",
        "color": "Green",
        "price": "1549.00",
        "description": "Soft green hoodie with a comfortable fit.",
        "image_url": "https://images.unsplash.com/photo-1620799140408-edc6dcb6d633?auto=format&fit=crop&w=900&q=80",
    },
]


def add_third_products(apps, schema_editor):
    ClothingCategory = apps.get_model("pages", "ClothingCategory")
    Product = apps.get_model("pages", "Product")

    for item in THIRD_PRODUCTS:
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


def remove_third_products(apps, schema_editor):
    Product = apps.get_model("pages", "Product")
    Product.objects.filter(name__in=[item["name"] for item in THIRD_PRODUCTS]).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_add_more_category_products"),
    ]

    operations = [
        migrations.RunPython(add_third_products, remove_third_products),
    ]
