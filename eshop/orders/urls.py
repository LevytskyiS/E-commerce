from django.urls import path

from . import views


app_name = "orders"
urlpatterns = [
    path("", views.OrderListView.as_view(), name="order_list"),
    # Shipping Address
    path(
        "shipping_address",
        views.ShippingAddressListView.as_view(),
        name="shipping_address_list",
    ),
    path(
        "update/shipping_address/<int:pk>/",
        views.ShippingAddressUpdateView.as_view(),
        name="update_shipping_address",
    ),
    path("order/<slug:slug>/", views.OrderDetailView.as_view(), name="order_detail"),
]
