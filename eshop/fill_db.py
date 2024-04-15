import os
import random
import math
import uuid

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
    Category,
    Subcategory,
    Brand,
    Product,
    Image,
    ProductImage,
)
from orders.models import Order, OrderItem, ShippingAddress, Nomenclature

# from users.models import Profile

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
categories = ["gents", "ladies"]
subcategories = ["hiking", "running", "gym", "outdoor"]
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

    admin = User.objects.create(
        username="admin",
        email="lol@gmail.com",
        first_name=faker.first_name(),
        last_name=faker.last_name(),
    )
    admin.is_staff = True
    admin.is_superuser = True
    admin.set_password("admin")
    admin.save()

    # Profile.objects.create(user=admin)

    for name in names:
        email = faker.email()
        password = faker.password()
        user = User.objects.create(
            username=name, email=email, first_name=name, last_name=faker.last_name()
        )
        user.set_password(password)
        user.save()
        # Profile.objects.create(user=user)


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


def create_categories(categories):
    for category in categories:
        Category.objects.create(name=category)


def create_subcategories(subcategories):
    categories = Category.objects.all()

    for subcategory in subcategories:
        obj = Subcategory.objects.create(name=subcategory)

        for category in categories:
            obj.category.add(category)
            obj.save()


def create_brands(brands):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()

    for brand in brands:
        obj = Brand.objects.create(name=brand)

        number_of_cats = random.randint(1, len(categories))
        number_of_subcats = random.randint(1, len(subcategories))

        celected_cats = set()
        celected_subcats = set()

        while len(celected_cats) < number_of_cats:
            celected_cats.add(random.choice(categories))

        for cat in celected_cats:
            obj.category.add(cat)
            obj.save()

        while len(celected_subcats) < number_of_subcats:
            celected_subcats.add(random.choice(subcategories))

        for subcat in celected_subcats:
            obj.subcategory.add(subcat)
            obj.save()


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
    names = [
        "Army men",
        "B-Daman",
        "Bakugan",
        "Digital pet",
        "Evel Knievel",
        "Funko",
        "G.I. Joe",
        "Gumby",
        "He-Man",
        "Jumping Jack",
        "Kenner Star Wars",
        "Lara",
        "Little People",
        "Monster",
        "Playmobil",
        "Power Rangers",
        "The Smurfs",
        "Stretch Armstrong",
        "TMNT",
        "Toy soldier",
        "Transformers",
        "Weebles",
    ]
    for name in names:
        sex = random.choice(["M", "W"])
        brand = random.choice(Brand.objects.all())
        if sex == "M":
            category = Category.objects.get(name="gents")
        else:
            category = Category.objects.get(name="ladies")
        subcategory = random.choice(Subcategory.objects.all())

        # price = random.choice([i for i in range(20, 200)])
        number_of_attributes = random.randint(2, 7)
        attributes = set()

        while len(attributes) < number_of_attributes:
            attributes.add(random.choice(Attribute.objects.all()))

        product = Product.objects.create(
            name=name, sex=sex, brand=brand, category=category, subcategory=subcategory
        )

        for attribute in attributes:
            product.attributes.add(attribute)
            product.save()


def create_nomenclatures():
    product_code = 100
    size_code = 10
    products = Product.objects.all()

    for product in products:
        number_of_nomenclatures = random.randint(2, 5)
        price = random.randint(10, 200)
        for _ in range(1, number_of_nomenclatures):
            nomenclature = Nomenclature.objects.create(
                code=f"{product_code}{size_code}",
                product=product,
                price=price,
                quantity_available=random.randint(1, 999),
            )
            size_code += 1
        product_code += 1


def creade_product_images():
    products = Product.objects.all()
    images = Image.objects.all()
    counter = 1

    for product in products:
        ProductImage.objects.create(
            name=f"Prod photo {counter}", product=product, image=random.choice(images)
        )


def create_shipping_address():
    users = User.objects.all()
    for user in users:
        address = (
            f"{faker.street_name()} {faker.building_number()}/{faker.building_number()}"
        )
        city = faker.city()
        postal_code = faker.postcode()

        ShippingAddress.objects.create(
            user=user,
            address=address,
            city=city,
            country="Czech Republic",
            postal_code=postal_code,
        )


def create_order():
    for i in range(100, 201):
        code = f"MM{i}"
        user = random.choice(User.objects.all())
        if user.shipping_addresses.all():
            Order.objects.create(
                code=code,
                user=user,
                shipping_address=random.choice(user.shipping_addresses.all()),
            )
        else:
            continue


def create_order_items():
    orders = Order.objects.all()

    for order in orders:
        number_of_products = random.randint(1, 5)

        for i in range(1, number_of_products + 1):
            nomenclature = random.choice(Nomenclature.objects.all())
            quantity = random.randint(1, 4)
            OrderItem.objects.create(
                order=order,
                nomenclature=nomenclature,
                quantity=quantity,
            )


# create_users()
# create_attribute_names(attr_names)
# create_attribute_values(attr_values)
# create_attributes(attr_names, attr_values)
# create_categories(categories)
# create_subcategories(subcategories)
# create_brands(brands)
# create_images()
# create_products()
# create_nomenclatures()
# creade_product_images()
# create_shipping_address()
# create_order()
# create_order_items()
