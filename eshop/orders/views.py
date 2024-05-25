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
from django.http import HttpRequest
from django.contrib.auth.models import User

from .models import Order, ShippingAddress
from .forms import CreateShippingAddressForm


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
        # return Order.objects.filter(user=self.request.user).order_by("created_at")
        return (
            Order.objects.filter(user=self.request.user)
            .select_related("user", "shipping_address")
            .prefetch_related("items__nomenclature")
            .order_by("created_at")
        )


# Shipping Address
class CreateShippingAddressView(CreateView):
    model = ShippingAddress
    form_class = CreateShippingAddressForm
    template_name = "orders/create_shipping_address.html"
    request = HttpRequest()

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)
        form.instance.user = user
        self.object = form.save()
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return reverse("users:profile", kwargs={"username": self.object.user.username})


class ShippingAddressListView(ListView):
    model = ShippingAddress
    template_name = "orders/shipping_address_list.html"
    context_object_name = "addresses"

    def get_queryset(self) -> QuerySet[ShippingAddress]:
        return (
            ShippingAddress.objects.filter(user=self.request.user)
            .filter(is_active=True)
            .select_related("user")
            .order_by("city")
        )


class ShippingAddressInactiveListView(ListView):
    model = ShippingAddress
    template_name = "orders/shipping_address_inactive_list.html"
    context_object_name = "addresses"

    def get_queryset(self) -> QuerySet[ShippingAddress]:
        return (
            ShippingAddress.objects.filter(user=self.request.user)
            .filter(is_active=False)
            .select_related("user")
            .order_by("city")
        )


class ShippingAddressUpdateView(UpdateView):
    model = ShippingAddress
    context_object_name = "shipping_address"
    fields = ["address", "city", "country", "postal_code", "is_active", "is_default"]
    template_name_suffix = "_update_form"

    def get_success_url(self) -> str:
        return reverse("orders:shipping_address_list")
