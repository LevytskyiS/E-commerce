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

from .models import Brand, Product, Category, Subcategory


class IndexView(View):
    def get(self, request):
        return render(request, "products/index.html")


# Brand
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
        return Brand.objects.all()


# Product
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
        return Product.objects.all()


class GentsProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(sex="M")


class LadiesProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(sex="W")


class GentsHikingProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="hiking")
            .filter(sex="M")
            .order_by("name")
        )


class LadiesHikingProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        print(len(Product.objects.filter(subcategory__name="hiking")))
        return (
            Product.objects.filter(subcategory__name="hiking")
            .filter(sex="W")
            .order_by("name")
        )


class GentsRunningProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="running")
            .filter(sex="M")
            .order_by("name")
        )


class LadiesRunningProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="running")
            .filter(sex="W")
            .order_by("name")
        )


class GentsGymProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="gym")
            .filter(sex="M")
            .order_by("name")
        )


class LadiesGymProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="gym")
            .filter(sex="W")
            .order_by("name")
        )
