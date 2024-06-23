from django.contrib import admin

from .models import CartItem, Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("id", "cart", "nomenclature", "quantity")
