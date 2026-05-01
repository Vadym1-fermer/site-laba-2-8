from django.db import migrations, models


PRODUCT_IMAGES = {
    "White T-shirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&w=900&q=80",
    "Blue Jeans": "https://images.unsplash.com/photo-1542272604-787c3835535d?auto=format&fit=crop&w=900&q=80",
    "Black Hoodie": "https://images.unsplash.com/photo-1556821840-3a63f95609a7?auto=format&fit=crop&w=900&q=80",
}


def add_product_images(apps, schema_editor):
    Product = apps.get_model("pages", "Product")

    for product_name, image_url in PRODUCT_IMAGES.items():
        Product.objects.filter(name=product_name).update(image_url=image_url)


def remove_product_images(apps, schema_editor):
    Product = apps.get_model("pages", "Product")
    Product.objects.update(image_url="")


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_seed_clothing_store_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="image_url",
            field=models.URLField(blank=True),
        ),
        migrations.RunPython(add_product_images, remove_product_images),
    ]
