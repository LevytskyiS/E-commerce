from django.db import models
from django.contrib.auth.models import User

from products.models import Product


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, related_name="shipping_addresses", on_delete=models.CASCADE
    )
    city = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    house_number = models.IntegerField()
    apartment = models.CharField(max_length=10)
    country_code = models.CharField(max_length=2)
    zipcode = models.CharField(max_length=8)


class Order(models.Model):
    # STATUS_CHOICES = (
    #     ("pending", "Pending"),
    # ("processing", "Processing"),
    #     ("completed", "Completed"),
    #     ("cancelled", "Cancelled"),
    # )
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        ShippingAddress, related_name="orders", on_delete=models.CASCADE
    )
    number = models.CharField(max_length=10, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        return self.number

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return (
            f"OrderItem {self.order}: Order {self.product.name} ({self.quantity} units)"
        )
