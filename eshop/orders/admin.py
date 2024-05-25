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
    search_fields = ("user__username", "address", "city", "country", "postal_code")
    # raw_id_fields = ("user",)
    autocomplete_fields = ("user",)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ("nomenclature",)
    autocomplete_fields = ("nomenclature",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "shipping_address",
        "code",
        "created_at",
        "updated_at",
    )
    list_filter = ("created_at", "updated_at", "user", "shipping_address")
    raw_id_fields = ("user", "shipping_address")
    search_fields = ("code", "user__username")
    date_hierarchy = "created_at"
    # list_select_related — это атрибут в Django Admin, который используется для оптимизации
    # запросов к базе данных при отображении связанных объектов в списках. Он позволяет вам
    # заранее загружать связанные объекты с использованием SQL JOIN, чтобы избежать выполнения
    # дополнительных запросов на каждую связанную запись.
    # list_select_related = ("user", "shipping_address")
    list_select_related = True
    inlines = [OrderItemInline]
    list_per_page = 20
    readonly_fields = ("user", "code")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "nomenclature", "quantity")
    search_fields = ("order__code", "nomenclature__code")
    list_filter = ("order", "nomenclature")
    autocomplete_fields = ("nomenclature", "order")
