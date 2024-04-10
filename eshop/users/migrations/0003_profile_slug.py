# Generated by Django 5.0.3 on 2024-04-06 19:50

import django_extensions.db.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_profile_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, populate_from='name'),
        ),
    ]