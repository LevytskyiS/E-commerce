from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from django.contrib.auth.models import User


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

        # if form_errors:
        #     messages.error(request, "There was an error updating your cart.")
        # else:
        #     messages.success(request, "Your cart was updated successfully.")

        return redirect("cart:cart_detail")


# class CartDetailView(ListView):
#     model = CartItem
#     template_name = "cart/cart_detail.html"
#     context_object_name = "cart_items"

#     def get_queryset(self):
#         cart, created = Cart.objects.get_or_create(user=self.request.user)
#         return cart.cart_items.all()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         cart = Cart.objects.get(user=self.request.user)
#         context["total_price"] = sum(
#             item.get_total_price() for item in cart.cart_items.all()
#         )
#         return context


class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        return render(request, "cart/checkout.html", {"cart": cart})

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        # Обработка заказа (например, создание записи в модели заказа)
        order = Order.objects.create(
            user=request.user, shipping_address=cart.shipping_address
        )
        for cart_item in cart.cart_items.all():
            nomenclature = Nomenclature.objects.get(code=cart_item.nomenclature)
            if cart_item.quantity <= nomenclature.quantity_available:
                nomenclature.quantity_available -= cart_item.quantity
                nomenclature.save()
                order_item = OrderItem.objects.create(
                    order=order, nomenclature=nomenclature, quantity=cart_item.quantity
                )
            else:
                error_occurred = True
                messages.error(
                    request,
                    f"Quantity for {nomenclature.product_variant.name} exceeds available stock.",
                )
                order.delete()
                # Need to inform a user, that a certain item is out of stock
                return redirect("cart:cart_detail")

        cart.cart_items.all().delete()
        return redirect("cart:order_confirmation")


class OrderConfirmationView(View):
    def get(self, request):
        return render(request, "cart/order_confirmation.html")
