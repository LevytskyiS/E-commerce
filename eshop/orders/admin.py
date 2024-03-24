from django.contrib import admin

from .models import ShippingAddress, Order, OrderItem


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "city",
        "street",
        "house_number",
        "apartment",
        "country_code",
        "zipcode",
    )
    list_filter = ("user",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "shipping_address",
        "number",
        "created_at",
        "updated_at",
    )
    list_filter = ("user", "shipping_address", "created_at", "updated_at")
    date_hierarchy = "created_at"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity")
