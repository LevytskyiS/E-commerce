import random

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from faker import Faker

from eshop.celery import app
from .models import Order, OrderItem, ShippingAddress
from products.models import Product

faker = Faker()


# @app.task
# def add_shipping_address():
#     number_of_addresses = random.randint(2, 5)
#     addresses = []

#     for _ in range(1, number_of_addresses + 1):
#         user = random.choice(User.objects.all())
#         city = faker.city()
#         street = faker.street_name()
#         house_number = int(faker.building_number())
#         apartment = faker.building_number()
#         country_code = faker.country_code()
#         zipcode = faker.postcode()

#         address = ShippingAddress.objects.create(
#             user=user,
#             city=city,
#             street=street,
#             house_number=house_number,
#             apartment=apartment,
#             country_code=country_code,
#             zipcode=zipcode,
#         )
#         addresses.append(model_to_dict(address))

#     return addresses


def create_order():
    address = random.choice(ShippingAddress.objects.all())
    user = random.choice(User.objects.all())

    try:
        order = Order.objects.create(
            shipping_address=address,
            user=user,
            number=f"KT{random.randint(100000, 999999)}",
        )
    except Exception as e:
        return None

    return order


def create_order_items(order: Order):
    number_of_poducts = random.randint(1, 15)
    products = set()
    order_items = []

    while len(products) < number_of_poducts:
        products.add(random.choice(Product.objects.all()))

    for product in products:
        order_item = OrderItem.objects.create(
            order=order, product=product, quantity=random.randint(1, 5)
        )
        order_items.append(model_to_dict(order_item))

    return order_items


@app.task
def place_order():
    number_of_orders = random.randint(1, 40)
    placed_orders = []

    for _ in range(0, number_of_orders + 1):
        order = create_order()
        if not order:
            continue
        order_items = create_order_items(order)
        placed_orders.append(
            {"order": model_to_dict(order), "order_items": order_items}
        )

    return placed_orders


@app.task
def create_users():
    number_of_new_users = random.randint(2, 5)
    new_users = []
    names = set()

    while len(names) < number_of_new_users:
        name = faker.first_name()
        names.add(name)

    for name in names:
        email = faker.email()
        password = faker.password()
        user = User.objects.create(username=name, email=email)
        user.set_password(password)
        user.save()
        new_users.append(model_to_dict(user))

    return new_users
