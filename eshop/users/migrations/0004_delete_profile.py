# Generated by Django 5.0.3 on 2024-04-06 20:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_slug'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]