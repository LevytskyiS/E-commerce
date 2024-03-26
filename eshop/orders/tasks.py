import random

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from celery import shared_task

from eshop.celery import app
from .models import Order, OrderItem, ShippingAddress
from products.models import Product, Brand


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
        print(e)
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
