from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    FormView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.models import User

from orders.models import Order


# Create your views here.
# User
class ProfileDetailView(DetailView):
    template_name = "users/user_detail.html"

    def get(self, request, username):
        # получаем пользователя по username если он существует
        user = get_object_or_404(User, username=username)
        # передаем его в шаблон как profile
        orders = Order.objects.filter(user=user)
        turnover = sum([order.total_price() for order in orders])
        return render(
            request, self.template_name, {"profile": user, "turnover": turnover}
        )


class ProfileUpdateView(UpdateView):
    model = User
    context_object_name = "user"
    fields = ["first_name", "last_name", "email"]
    template_name = "users/user_update_form.html"

    def get_success_url(self):
        return reverse("users:profile", kwargs={"username": self.object.username})
