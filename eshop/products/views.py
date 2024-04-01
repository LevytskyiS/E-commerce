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

from .models import Brand, Product


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
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Brand]:
        brands = Brand.objects.all()
        sublists = [brands[i : i + 3] for i in range(0, len(brands), 3)]
        return sublists


class ProductDetailView(DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        products = Product.objects.all()
        sublists = [products[i : i + 3] for i in range(0, len(products), 3)]
        return sublists
