from typing import Any
from django.db.models.query import QuerySet
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

from .models import Brand


class IndexView(View):
    def get(self, request):
        return render(request, "products/index.html")


class BrandDetailView(DetailView):
    model = Brand
    template_name = "products/brand_detail.html"
    context_object_name = "brand"


class BrandListView(ListView):
    model = Brand
    template_name = "products/brand_list.html"
    context_object_name = "brands"
    paginate_by = 10

    def get_queryset(self) -> QuerySet[Brand]:
        return Brand.objects.all()
