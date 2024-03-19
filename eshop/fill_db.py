import os

import django
import requests

from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
# Call the django.setup() function before accessing Django settings.
django.setup()

from products.models import AttributeName, AttributeValue, Attribute

attr_names = ["color", "certificate"]
attr_values = [
    {
        "color": [
            "red",
            "green",
            "yellow",
            "black",
            "white",
            "blue",
            "gray",
            "orange",
        ]
    },
    {"certificate": ["OEKO", "TEX", "WTF-6", "OMG"]},
]


def create_attribute_names(names):
    for name in names:
        AttributeName.objects.create(name=name)


def create_attribute_values(attr_values: list) -> None:

    for attr_value in attr_values:
        for value in attr_value.values():
            for item in value:
                requests.post(
                    "http://127.0.0.1:8000/api/v1/attributevalue/", data={"value": item}
                )


def create_attributes(names, values):
    """Create attributes and their values"""
    for name in names:

        for data in values:
            attributes = data.get(name)

            if not attributes:
                continue

            attr_name = AttributeName.objects.get(name=name)

            for attribute in attributes:
                attr_value = AttributeValue.objects.get(value=attribute)
                attribute = Attribute.objects.create(
                    attribute_name=attr_name, attribute_value=attr_value
                )
                attribute.save()


# create_attribute_names(attr_names)
# create_attribute_values(attr_values)
# create_attributes(attr_names, attr_values)
