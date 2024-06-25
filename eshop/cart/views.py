from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View

from .models import CartItem, Cart


class CartDetailView(ListView):
    model = CartItem
    template_name = "cart/cart_detail.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart.cart_items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart.objects.get(user=self.request.user)
        context["total_price"] = sum(
            item.get_total_price() for item in cart.cart_items.all()
        )
        return context


class CheckoutView(View):
    def get(self, request):
        cart = Cart.objects.get(user=request.user)
        return render(request, "cart/checkout.html", {"cart": cart})

    def post(self, request):
        cart = Cart.objects.get(user=request.user)
        # Обработка заказа (например, создание записи в модели заказа)
        cart.cart_items.all().delete()
        return redirect("cart:order_confirmation")


class OrderConfirmationView(View):
    def get(self, request):
        return render(request, "cart/order_confirmation.html")
