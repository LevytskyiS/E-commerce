from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.urls import reverse
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


class ShippingAddressUpdateView(UpdateView):
    model = ShippingAddress
    context_object_name = "shipping_address"
    fields = ["address", "city", "country", "postal_code", "is_active", "is_default"]
    template_name_suffix = "_update_form"

    def get_success_url(self) -> str:
        print(self.__dict__)
        return reverse("orders:shipping_address_list")
