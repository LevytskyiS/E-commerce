# Generated by Django 5.0.3 on 2024-06-16 09:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_nomenclature_attributes'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='product_variant',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='product_variant_image', to='products.productvariant'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
