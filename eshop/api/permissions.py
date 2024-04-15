from rest_framework import permissions

from orders.models import Order


class IsOrderCreatorOrAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        order = Order.objects.get(id=view.kwargs["pk"])
        if request.user.id == order.user.id or request.user.is_staff:
            return True
