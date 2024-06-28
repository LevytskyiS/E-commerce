from typing import Any

from django.db.models.query import QuerySet
from django.db.models import Prefetch
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

from .models import Order, ShippingAddress, OrderItem, Nomenclature
from .forms import CreateShippingAddressForm, UpdateShippingAddressForm
from products.models import Attribute


# Order
class OrderDetailView(DetailView):
    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"

    def get_queryset(self) -> QuerySet[Any]:
        order = Order.objects.select_related(
            "user",
            "shipping_address",
        ).prefetch_related(
            Prefetch(
                "items",
                queryset=OrderItem.objects.select_related(
                    "nomenclature",
                ),
            ),
        )
        return order


class OrderListView(ListView):
    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self) -> QuerySet[Order]:
        if not self.request.user.is_authenticated:
            return reverse("products:index")
        # return Order.objects.filter(user=self.request.user).order_by("created_at")
        return (
            Order.objects.filter(user=self.request.user)
            .select_related("user", "shipping_address")
            .prefetch_related("items__nomenclature")
            .order_by("-created_at")
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
    form_class = UpdateShippingAddressForm
    template_name_suffix = "_update_form"

    def get_success_url(self) -> str:
        return reverse("orders:shipping_address_list")

    # model = ShippingAddress
    # form_class = CreateShippingAddressForm
    # template_name = "orders/create_shipping_address.html"
    # request = HttpRequest()

    # def form_valid(self, form):
    #     user = User.objects.get(id=self.request.user.id)
    #     form.instance.user = user
    #     self.object = form.save()
    #     return super().form_valid(form)

    # def get_success_url(self) -> str:
    #     return reverse("users:profile", kwargs={"username": self.object.user.username})
