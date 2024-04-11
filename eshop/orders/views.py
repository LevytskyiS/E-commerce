from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    FormView,
    UpdateView,
    DeleteView,
)

from .models import Order, ShippingAddress


# Order
class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self) -> QuerySet[Order]:
        return Order.objects.filter(user=self.request.user).order_by("created_at")


# Shipping Address
class ShippingAddressListView(ListView):
    model = ShippingAddress
    template_name = "orders/shipping_address_list.html"
    context_object_name = "addresses"

    def get_queryset(self) -> QuerySet[ShippingAddress]:
        return ShippingAddress.objects.filter(user=self.request.user).order_by("city")
