import os
import random

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
    AttributeImage,
    Attribute,
    Category,
    Subcategory,
    Brand,
    Product,
    ProductVariant,
    Image,
)
from orders.models import Order, OrderItem, ShippingAddress, Nomenclature, PaymentMethod

# from users.models import Profile

from productsd import products_data

faker = Faker()
attr_names = ["certificate", "size", "color", "material", "properties"]
attr_values = [
    {
        "certificate": [
            "Eco-Friendly Fabric Certification",
            "Fair Trade Apparel Certification",
            "Organic Cotton Standard",
            "Non-Toxic Dye Certification",
            "Sustainable Manufacturing Seal",
        ]
    },
    {"size": ["XS", "S", "M", "L", "XL", "2XL", "3XL"]},
    {"color": ["Black", "White", "Red", "Blue", "Green", "Yellow"]},
    {
        "material": [
            "100% cotton",
            "100% polyester",
            "50% cotton, 50% polyester",
            "softshell",
        ]
    },
    {
        "properties": [
            "Breathable",
            "Water-Resistant",
            "Wrinkle-Free",
            "Stretchable",
            "Quick-Drying",
            "Moisture-Wicking",
            "Hypoallergenic",
            "Thermal Insulation",
            "UV Protection",
            "Anti-Microbial",
        ]
    },
]

color_images = [
    {
        "Black": "https://i1.wp.com/cornellsun.com/wp-content/uploads/2020/06/1591119073-screen_shot_2020-06-02_at_10.30.13_am.png?fit=700%2C652&ssl=1"
    },
    {
        "White": "https://dragonimage.com.au/cdn/shop/products/image36_4_1.jpg?v=1637899806"
    },
    {"Red": "https://w0.peakpx.com/wallpaper/195/332/HD-wallpaper-red-plain.jpg"},
    {"Blue": "https://i.pinimg.com/736x/d7/4c/e3/d74ce3c8f1accd04ba44bdf18781a593.jpg"},
    {
        "Green": "https://pub-static.fotor.com/assets/bg/246400f6-8a87-48ad-9698-281d55b388f5.jpg"
    },
    {
        "Yellow": "https://img.freepik.com/free-photo/vivid-blurred-colorful-wallpaper-background_58702-5912.jpg"
    },
]

categories = ["gents", "ladies", "kids"]
subcategories = ["t-shirt", "shirt", "polo shirt", "jacket", "top"]
brands = [
    {"UrbanTrend": [[1, 2], [2, 3]]},
    {"VogueVista": [[2, 3], [1, 2, 3]]},
    {"Eclipse Apparel": [[1, 3], [4, 5]]},
    {"Fabrica Luxe": [[1, 2, 3], [3, 4, 4]]},
    {"ChicStreet": [[2, 3], [1, 4, 5]]},
]

brands_images = [
    {
        "UrbanTrend": "https://cdn.shopify.com/s/files/1/2224/0955/files/UrbanTrnd_Logo.png?height=628&pad_color=fff&v=1613154939&width=1200"
    },
    {
        "VogueVista": "https://vogue-vista.shop/cdn/shop/files/Vogue_Vista-4.png?height=628&pad_color=f8f8f8&v=1704562729&width=1200"
    },
    {
        "Eclipse Apparel": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSjA0zjzay2HpHJoR_3yJr62kpyzKvj1qEZPQ&s"
    },
    {
        "Fabrica Luxe": "https://seeklogo.com/images/L/luxury-logo-C88D07841D-seeklogo.com.png"
    },
    {
        "ChicStreet": "https://chicstreet.com/cdn/shop/files/logo_1200x1200.jpg?v=1613712202"
    },
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


def create_attribute_images():
    for data in color_images:
        for key, value in data.items():
            AttributeImage.objects.create(name=key, image=value)


def add_attribute_image():
    attrs = Attribute.objects.filter(attribute_name__name="color")
    colors_images = AttributeImage.objects.all()
    for attr in attrs:
        for color_data in colors_images:
            if attr.attribute_value.value == color_data.name:
                attr.attribute_image = color_data
                attr.save()


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


def create_brands(brands: list):
    for brand_data in brands:
        for key, value in brand_data.items():
            brand = Brand.objects.create(name=key)
            categories_id = value[0]
            subcategories_id = value[1]

            for cat_id in categories_id:
                category = Category.objects.get(id=cat_id)
                brand.category.add(category)
                brand.save()

            for subcat_id in subcategories_id:
                subcategory = Subcategory.objects.get(id=subcat_id)
                brand.subcategory.add(subcategory)
                brand.save()


def add_brand_image():
    for data in brands_images:
        for key, value in data.items():
            brand = Brand.objects.get(name=key)
            brand.image = value
            brand.save()


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


def create_payment_methods():
    pass


def create_products_productvariants_nomenclatures():
    for prod_data in products_data:
        product = prod_data["product"]
        attributes = product["attributes"]

        product_obj = Product.objects.create(
            name=product["name"],
            sex=product["sex"],
            category=Category.objects.get(id=product["category"]),
            subcategory=Subcategory.objects.get(id=product["subcategory"]),
            brand=Brand.objects.get(id=product["brand"]),
        )

        for attribute_id in attributes:
            attribute = Attribute.objects.get(id=attribute_id)
            product_obj.attributes.add(attribute)
            product_obj.save()

        product_variants: list = product["product_variants"]

        for product_variant in product_variants:
            product_variant_data = product_variant["product_variant"]
            product_variant_obj = ProductVariant.objects.create(
                product=product_obj,
                name=product_variant_data["name"],
                attributes=Attribute.objects.get(id=product_variant_data["attributes"]),
                price=product_variant_data["price"],
                description=product_variant_data["description"],
            )

            images = product_variant_data["images"]

            for image in images:
                image_obj = Image.objects.create(
                    name=product_variant_obj.name,
                    image=image,
                    product_variant=product_variant_obj,
                )

            nomenclatures = product_variant_data["nomenclatures"]

            for nomenclature in nomenclatures:
                nomenclature_data = nomenclature["nomenclature"]
                nomenclature_obj = Nomenclature.objects.create(
                    code=nomenclature_data["code"],
                    product_variant=product_variant_obj,
                    price=nomenclature_data["price"],
                    quantity_available=nomenclature_data["quantity_available"],
                    attributes=Attribute.objects.get(
                        id=nomenclature_data["attributes"]
                    ),
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


def create_payment_methos():
    PaymentMethod.objects.create(name="AP")


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


create_users()
create_attribute_names(attr_names)
create_attribute_values(attr_values)
create_attributes(attr_names, attr_values)
create_attribute_images()
add_attribute_image()
create_categories(categories)
create_subcategories(subcategories)
create_brands(brands)
add_brand_image()
create_payment_methods()
create_products_productvariants_nomenclatures()

# create_nomenclatures()
# creade_product_images()
# create_shipping_address()
# create_payment_methos()
# create_order()
# create_order_items()
