from rest_framework import permissions

from orders.models import Order, ShippingAddress


class IsOrderCreatorOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        order = Order.objects.get(id=view.kwargs.get("pk"))

        if request.user.id == order.user.id or request.user.is_staff:
            return True


class IsShippingAddressCreatorOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        address = ShippingAddress.objects.get(id=view.kwargs.get("pk"))

        if request.user.id == address.user.id or request.user.is_staff:
            return True
