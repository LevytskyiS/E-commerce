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
attr_names = ["color", "certificate", "details"]
attr_values = [
    {
        "color": [
            "Absolute Zero",
            "Acid green",
            "Aero",
            "African violet",
            "Air superiority blue",
            "Alice blue",
            "Alizarin",
            "Alloy orange",
            "Almond",
            "Amaranth deep purple",
            "Amaranth pink",
            "Amaranth purple",
            "Amazon",
            "Amber",
            "Amethyst",
            "Android green",
            "Antique brass",
            "Antique bronze",
            "Antique fuchsia",
            "Antique ruby",
            "Antique white",
            "Apricot",
            "Aqua",
            "Aquamarine",
            "Arctic lime",
            "Artichoke green",
            "Arylide yellow",
            "Ash gray",
            "Atomic tangerine",
            "Aureolin",
            "Azure",
            "Azure (X11/web color)",
            "Baby blue",
            "Baby blue eyes",
            "Baby pink",
            "Baby powder",
            "Baker-Miller pink",
            "Banana Mania",
            "Barbie Pink",
            "Barn red",
            "Battleship grey",
            "Beau blue",
            "Beaver",
            "Beige",
            "B'dazzled blue",
            "Big dip o'ruby",
            "Bisque",
            "Bistre",
            "Bistre brown",
            "Bitter lemon",
            "Black",
            "Black bean",
            "Black coral",
            "Black olive",
            "Black Shadows",
            "Blanched almond",
            "Blast-off bronze",
            "Bleu de France",
            "Blizzard blue",
            "Blood red",
            "Blue",
            "Blue (Crayola)",
            "Blue (Munsell)",
            "Blue (NCS)",
            "Blue (Pantone)",
            "Blue (pigment)",
            "Blue bell",
            "Blue-gray\xa0(Crayola)",
            "Blue jeans",
            "Blue sapphire",
            "Blue-violet",
            "Blue yonder",
            "Bluetiful",
            "Blush",
            "Bole",
            "Bone",
            "Brick red",
            "Bright lilac",
            "Bright yellow (Crayola)",
            "British racing green",
            "Bronze",
            "Brown",
            "Brown sugar",
            "Bud green",
            "Buff",
            "Burgundy",
            "Burlywood",
            "Burnished brown",
            "Burnt orange",
            "Burnt sienna",
            "Burnt umber",
            "Byzantine",
            "Byzantium",
            "Cadet blue",
            "Cadet grey",
            "Cadmium green",
            "Cadmium orange",
            "Café au lait",
            "Café noir",
            "Cambridge blue",
            "Camel",
            "Cameo pink",
            "Canary",
            "Canary yellow",
            "Candy pink",
            "Cardinal",
            "Caribbean green",
            "Carmine",
            "Carnation pink",
            "Carnelian",
            "Carolina blue",
            "Carrot orange",
            "Catawba",
            "Cedar Chest",
            "Celadon",
            "Celeste",
            "Cerise",
            "Cerulean",
            "Cerulean blue",
            "Cerulean frost",
            "Champagne",
            "Champagne pink",
            "Charcoal",
            "Charm pink",
            "Chartreuse",
            "Cherry blossom pink",
            "Chestnut",
            "Chili red",
            "China pink",
            "Chinese red",
            "Chinese violet",
            "Chinese yellow",
            "Chocolate (traditional)",
            "Chocolate (web)",
            "Cinereous",
            "Cinnabar",
            "Cinnamon Satin",
            "Citrine",
            "Citron",
            "Claret",
            "Coffee",
            "Columbia Blue",
            "Congo pink",
            "Cool grey",
            "Copper",
            "Copper penny",
            "Copper red",
            "Copper rose",
            "Coquelicot",
            "Coral",
            "Coral pink",
            "Cordovan",
            "Corn",
            "Cornflower blue",
            "Cornsilk",
            "Cosmic cobalt",
            "Cosmic latte",
            "Coyote brown",
            "Cotton candy",
            "Cream",
            "Crimson",
            "Cultured Pearl",
            "Cyan",
            "Cyan (process)",
            "Cyber grape",
            "Cyber yellow",
            "Cyclamen",
            "Dandelion",
            "Dark brown",
            "Dark byzantium",
            "Dark cyan",
            "Dark electric blue",
            "Dark goldenrod",
            "Dark green",
            "Dark jungle green",
            "Dark khaki",
            "Dark lava",
            "Dark liver",
            "Dark magenta",
            "Dark olive green",
            "Dark orange",
            "Dark orchid",
            "Dark purple",
            "Dark red",
            "Dark salmon",
            "Dark sea green",
            "Dark sienna",
            "Dark sky blue",
            "Dark slate blue",
            "Dark slate gray",
            "Dark spring green",
            "Dark turquoise",
            "Dark violet",
            "Davy's grey",
            "Deep cerise",
            "Deep champagne",
            "Deep chestnut",
            "Deep jungle green",
            "Deep pink",
            "Deep saffron",
            "Deep sky blue",
            "Deep Space Sparkle",
            "Deep taupe",
            "Denim",
            "Denim blue",
            "Desert",
            "Desert sand",
            "Dim gray",
            "Dodger blue",
            "Drab dark brown",
            "Duke blue",
            "Dutch white",
            "Ebony",
            "Ecru",
            "Eerie black",
            "Eggplant",
            "Eggshell",
            "Electric lime",
            "Electric purple",
            "Electric violet",
            "Emerald",
            "Eminence",
            "English lavender",
            "English red",
            "English vermillion",
            "English violet",
            "Erin",
            "Eton blue",
            "Fallow",
            "Falu red",
            "Fandango",
            "Fandango pink",
            "Fawn",
            "Fern green",
            "Field drab",
            "Fiery rose",
            "Finn",
            "Firebrick",
            "Fire engine red",
            "Flame",
            "Flax",
            "Flirt",
            "Floral white",
            "Forest green",
            "French beige",
            "French bistre",
            "French blue",
            "French fuchsia",
            "French lilac",
            "French lime",
            "French mauve",
            "French pink",
            "French raspberry",
            "French sky blue",
            "French violet",
            "Frostbite",
            "Fuchsia",
            "Fulvous",
            "Fuzzy Wuzzy",
        ]
    },
    {"certificate": ["OEKO", "TEX", "WTF-6", "OMG"]},
    {
        "details": [
            "Regular fit",
            "Lace closure",
            "Mesh upper",
            "Stable, responsive feel",
            "Textile lining",
            "Lightstrike cushioning",
            "Adiwear outsole",
            "Upper contains a minimum of 50% recycled content",
            "Imported",
        ]
    },
]
brands = [
    "Nike",
    "Abibas",
    "Converse",
    "Under Armour",
    "Reebok",
    "New Balance",
    "Abricot",
    "Agnello",
    "Alba",
    "Bershka",
    "Carrera",
    "Fendi",
    "Gucci",
    "Hermes",
    "YSL",
]


def create_users():
    names = set()

    while len(names) < 10:
        name = faker.first_name()
        names.add(name)

    admin = User.objects.create(username="admin", email="lol@gmail.com")
    admin.is_staff = True
    admin.is_superuser = True
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
        number_of_attributes = random.randint(2, 7)
        attributes = set()

        while len(attributes) < number_of_attributes:
            attributes.add(random.choice(Attribute.objects.all()))

        product = Product.objects.create(name=name, brand=brand, price=price)

        for attribute in attributes:
            product.attributes.add(attribute)
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
