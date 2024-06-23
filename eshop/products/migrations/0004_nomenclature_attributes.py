# Generated by Django 5.0.3 on 2024-06-16 08:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_productvariant_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='nomenclature',
            name='attributes',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='nomenclature', to='products.attribute'),
            preserve_default=False,
        ),
    ]