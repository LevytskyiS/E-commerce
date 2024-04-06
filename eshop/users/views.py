from typing import Any

from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
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

from .models import Profile


# Create your views here.
# User
class UserDetailView(DetailView):
    model = User
    template_name = "users/user_detail.html"
