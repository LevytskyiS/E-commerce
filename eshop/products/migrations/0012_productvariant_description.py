# Generated by Django 5.0.3 on 2024-06-25 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_attribute_attribute_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='productvariant',
            name='description',
            field=models.CharField(default=1),
            preserve_default=False,
        ),
    ]
