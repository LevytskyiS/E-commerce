# Generated by Django 5.0.3 on 2024-06-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='brand',
            name='image',
            field=models.URLField(null=True, unique=True),
        ),
    ]