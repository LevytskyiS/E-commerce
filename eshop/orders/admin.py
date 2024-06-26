from django.contrib import admin

from .models import (
    ShippingAddress,
    Order,
    OrderItem,
    Invoice,
    PaymentMethod,
)


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
    search_fields = ("user__username", "address", "city", "country", "postal_code")
    autocomplete_fields = ("user",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("nomenclature",)
    autocomplete_fields = ("nomenclature",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "payment_method",
        "user",
        "total_order_price",
        "shipping_address",
        "code",
        "created_at",
        # "updated_at",
    )
    list_filter = ("created_at", "user", "shipping_address")
    raw_id_fields = ("shipping_address",)
    search_fields = ("code", "user__username")
    date_hierarchy = "created_at"
    list_select_related = True
    inlines = [OrderItemInline]
    list_per_page = 20
    readonly_fields = ("code",)

    def total_order_price(self, obj: Order):
        return obj.total_price()

    total_order_price.short_description = "Total Price"


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "nomenclature", "quantity")
    search_fields = ("order__code", "nomenclature__code")
    list_filter = ("order", "nomenclature")
    autocomplete_fields = ("nomenclature", "order")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "number")
    search_fields = ("order__code", "number")
    autocomplete_fields = ("order",)


@admin.register(PaymentMethod)
class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
