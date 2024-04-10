from django.urls import path

from . import views


app_name = "orders"
urlpatterns = [
    path("order/<slug:slug>/", views.OrderDetailView.as_view(), name="order_detail"),
]
