# Generated by Django 5.0.3 on 2024-06-17 16:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_nomenclature_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attribute',
            name='attribute_image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='attribute', to='products.attributeimage'),
        ),
    ]
