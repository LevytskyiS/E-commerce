# Generated by Django 5.0.3 on 2024-06-16 08:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_productvariant_colors'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productvariant',
            options={'verbose_name': 'Product Variant', 'verbose_name_plural': 'Product Variants'},
        ),
        migrations.RenameField(
            model_name='productvariant',
            old_name='colors',
            new_name='attributes',
        ),
    ]