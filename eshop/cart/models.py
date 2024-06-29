from django.db import models
from django.contrib.auth.models import User

from products.models import Nomenclature
from orders.models import ShippingAddress


# Create your models here.
class Cart(models.Model):
    user = models.OneToOneField(User, related_name="cart", on_delete=models.CASCADE)
    shipping_address = models.OneToOneField(
        ShippingAddress, on_delete=models.CASCADE, related_name="cart", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    nomenclature = models.ForeignKey(Nomenclature, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def get_total_price(self):
        return self.quantity * self.nomenclature.price
