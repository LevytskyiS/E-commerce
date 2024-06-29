from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction


from .models import CartItem, Cart
from .forms import CartItemForm
from products.models import Nomenclature
from orders.models import Order, OrderItem, ShippingAddress


class CartDetailView(View):
    def get(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        cart_items = cart.cart_items.all()
        for item in cart_items:
            if item.quantity == 0:
                item.delete()
        cart_item_forms = [
            (item, CartItemForm(instance=item, prefix=str(item.id)))
            for item in cart_items
        ]
        total_price = sum(item.get_total_price() for item in cart_items)
        return render(
            request,
            "cart/cart_detail.html",
            {
                "cart": cart,
                "cart_item_forms": cart_item_forms,
                "total_price": total_price,
                "addresses": request.user.shipping_addresses.filter(is_active=True),
            },
        )

    def post(self, request):
        cart = get_object_or_404(Cart, user=request.user)
        address = ShippingAddress.objects.get(id=request.POST.get("address_id"))
        cart.shipping_address = address
        cart.save()
        cart_items = cart.cart_items.all()
        form_errors = False

        for item in cart_items:
            form = CartItemForm(request.POST, instance=item, prefix=str(item.id))
            if form.is_valid():
                form.save()
            else:
                form_errors = True

        return redirect("cart:cart_detail")


class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        return render(request, "cart/checkout.html", {"cart": cart})

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        order = Order(user=request.user, shipping_address=cart.shipping_address)

        order_items = []

        with transaction.atomic():

            for item in cart.cart_items.all():
                nomenclature: Nomenclature = item.nomenclature

                if item.quantity <= nomenclature.quantity_available:
                    nomenclature.quantity_available -= item.quantity
                    order_item = OrderItem(
                        order=order, nomenclature=nomenclature, quantity=item.quantity
                    )
                    nomenclature.save()
                    order_items.append(order_item)

                else:
                    error_occurred = True
                    messages.error(
                        request,
                        f"Quantity for {nomenclature.product_variant.name} exceeds available stock.",
                    )
                    return redirect("cart:cart_detail")

            order.save()
            OrderItem.objects.bulk_create(order_items)

        cart.cart_items.all().delete()
        cart.shipping_address = None
        cart.save()
        return redirect("cart:order_confirmation")


class OrderConfirmationView(View):
    def get(self, request):
        return render(request, "cart/order_confirmation.html")
