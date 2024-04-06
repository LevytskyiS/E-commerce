# Generated by Django 5.0.3 on 2024-04-04 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_brand_category_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sex',
            field=models.CharField(choices=[('M', 'Men'), ('W', 'Women')], default=1, max_length=1),
            preserve_default=False,
        ),
    ]
