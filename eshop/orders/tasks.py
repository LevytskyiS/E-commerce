import random

from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from celery import shared_task

from eshop.celery import app
from .models import Order, OrderItem, ShippingAddress
from products.models import Product, Brand


@app.task
def place_order():
    ship_address = ShippingAddress.objects.first()
    user = User.objects.first()

    try:
        order = Order.objects.create(
            shipping_address=ship_address,
            user=user,
            number=f"KT{random.randint(100000, 999999)}",
        )
    except Exception as e:
        print(e)
        return "Something went wrong!"

    return model_to_dict(order)
