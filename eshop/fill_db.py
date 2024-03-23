import os
import random
import math

import django
import requests

from django.conf import settings
from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eshop.settings")
# Call the django.setup() function before accessing Django settings.
django.setup()

from django.contrib.auth.models import User

from eshop.settings import PIXABAY_API_KEY
from products.models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Brand,
    Product,
    Image,
    ProductImage,
)
from orders.models import Order, OrderItem, ShippingAddress


faker = Faker()
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
brands = [
    "Nike",
    "Abibas",
    "Converse",
    "Under Armour",
    "Reebok",
    "New Balance",
]


def create_users():
    names = set()

    while len(names) < 10:
        name = faker.first_name()
        names.add(name)

    admin = User.objects.create(username="admin", email="lol@gmail.com")
    admin.set_password("admin")
    admin.save()

    for name in names:
        email = faker.email()
        password = faker.password()
        user = User.objects.create(username=name, email=email)
        user.set_password(password)
        user.save()


def create_attribute_names(names):
    for name in names:
        AttributeName.objects.create(name=name)


def create_attribute_values(attr_values: list) -> None:

    for attr_value in attr_values:
        for value in attr_value.values():
            for item in value:
                AttributeValue.objects.create(value=item)
                # requests.post(
                #     "http://127.0.0.1:8000/api/v1/attributevalue/", data={"value": item}
                # )


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


def create_brands(brands):
    for brand in brands:
        Brand.objects.create(name=brand)


def create_images():
    response = requests.get(
        f"https://pixabay.com/api/?key={PIXABAY_API_KEY}&q=fashion&image_type=photo"
    )
    hits = response.json()["hits"]
    counter = 1

    for data in hits:
        image = data.get("largeImageURL")
        name = f"image{counter}"
        Image.objects.create(name=name, image=image)
        counter += 1


def create_products():
    code = "TX"
    for i in range(1, 51):
        name = f"{code}{i}"
        brand = random.choice(Brand.objects.all())
        price = random.choice([i for i in range(20, 200)])
        attibute = random.choice(Attribute.objects.all())
        product = Product.objects.create(name=name, brand=brand, price=price)
        product.attributes.add(attibute)
        product.save()


def creade_product_images():
    products = Product.objects.all()
    images = Image.objects.all()
    counter = 1

    for product in products:
        ProductImage.objects.create(
            name=f"Prod photo {counter}", product=product, image=random.choice(images)
        )


def create_shipping_address():
    for _ in range(10):
        user = random.choice(User.objects.all())
        city = faker.city()
        street = faker.street_name()
        house_number = int(faker.building_number())
        apartment = faker.building_number()
        country_code = faker.country_code()
        zipcode = faker.postcode()

        ShippingAddress.objects.create(
            user=user,
            city=city,
            street=street,
            house_number=house_number,
            apartment=apartment,
            country_code=country_code,
            zipcode=zipcode,
        )
    # city = models.CharField(max_length=256)
    # street = models.CharField(max_length=256)
    # house_number = models.IntegerField()
    # apartment = models.CharField(max_length=10)
    # country_code = models.CharField(max_length=2)
    # zipcode = models.CharField(max_length=8)


def create_order():
    for i in range(100, 121):
        number = f"KT{i}"
        Order.objects.create(
            number=number,
            user=random.choice(User.objects.all()),
            shipping_address=random.choice(ShippingAddress.objects.all()),
        )


def create_order_items():
    orders = Order.objects.all()

    for order in orders:
        number_of_products = random.randint(1, 5)

        for i in range(1, number_of_products + 1):
            product = random.choice(Product.objects.all())
            quantity = random.randint(1, 4)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
            )


create_users()
create_attribute_names(attr_names)
create_attribute_values(attr_values)
create_attributes(attr_names, attr_values)
create_brands(brands)
create_images()
create_products()
creade_product_images()
create_shipping_address()
create_order()
create_order_items()
