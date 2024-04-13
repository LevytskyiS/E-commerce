from django.contrib import admin

from .models import ShippingAddress, Order, OrderItem


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "address",
        "city",
        "country",
        "postal_code",
        "is_default",
        "is_active",
    )
    list_filter = ("user", "is_default", "is_active")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "shipping_address",
        "code",
        "slug",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at")
    raw_id_fields = ("user", "shipping_address")
    search_fields = ("slug",)
    date_hierarchy = "created_at"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "nomenclature", "quantity")
    raw_id_fields = ("order", "nomenclature")
