from django.urls import path
from .views import (
    CartDetailView,
    CheckoutView,
    OrderConfirmationView,
)

app_name = "cart"
urlpatterns = [
    # path(
    #     "product-variant/<int:pk>/",
    #     ProductVariantDetailView.as_view(),
    #     name="product_variant_detail",
    # ),
    path("my-cart/", CartDetailView.as_view(), name="cart_detail"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path(
        "order-confirmation/",
        OrderConfirmationView.as_view(),
        name="order_confirmation",
    ),
]
