from django.core.cache import cache
from django.db.models import Prefetch
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

from .models import Brand, Product, Attribute


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
        return Brand.objects.order_by("name")


# Product
class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = "product_slug"
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related(
            "brand", "category", "subcategory"
        ).prefetch_related(
            "attributes__attribute_name",
            "attributes__attribute_value",
            # "product_image__image",
        )

        # select_related - предзагружает поля, которые являются FK
        # prefetch_related - предзагружает дочерние объекты поля


class ProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # colors = cache.get("colors")
        # if not colors:
        #     colors = Attribute.objects.filter(
        #         attribute_name__name="color"
        #     ).select_related("attribute_value")
        #     cache.set("colors", colors, 3600)  # Кэш на 1 час
        colors = Attribute.objects.filter(attribute_name__name="color").select_related(
            "attribute_value"
        )
        certificates = Attribute.objects.filter(
            attribute_name__name="certificate"
        ).select_related("attribute_value")

        context["colors"] = colors
        context["certificates"] = certificates

        return context

    def get_queryset(self) -> QuerySet[Product]:
        queryset = Product.objects.all().select_related(
            "brand", "category", "subcategory"
        )
        queryset = queryset.prefetch_related(
            Prefetch(
                "attributes",
                queryset=Attribute.objects.select_related(
                    "attribute_name", "attribute_value"
                ),
            )
        )

        brands = self.request.GET.getlist("brand")
        colors = self.request.GET.getlist("color")
        certificates = self.request.GET.getlist("certificate")

        print(colors)

        if brands:
            queryset = queryset.filter(brand__name__in=brands)

        if colors:
            queryset = queryset.filter(
                attributes__attribute_value__value__in=colors,
            )

        if certificates:
            queryset = queryset.filter(
                attributes__attribute_value__value__in=certificates,
            )

        return queryset


class GentsProductListView(ListView):
    model = Product
    template_name = "products/gents_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(sex="M").select_related(
            "brand", "category", "subcategory"
        )


class LadiesProductListView(ListView):
    model = Product
    template_name = "products/ladies_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return Product.objects.filter(sex="W").select_related(
            "brand", "category", "subcategory"
        )


class HikingProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="hiking")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class RunningProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="running")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class GymProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="gym")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class OutdoorProductListView(ListView):
    model = Product
    template_name = "products/product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="outdoor")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class GentsHikingProductListView(ListView):
    model = Product
    template_name = "products/gents_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="hiking")
            .filter(sex="M")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class LadiesHikingProductListView(ListView):
    model = Product
    template_name = "products/ladies_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        print(len(Product.objects.filter(subcategory__name="hiking")))
        return (
            Product.objects.filter(subcategory__name="hiking")
            .filter(sex="W")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class GentsRunningProductListView(ListView):
    model = Product
    template_name = "products/gents_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="running")
            .filter(sex="M")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class LadiesRunningProductListView(ListView):
    model = Product
    template_name = "products/ladies_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="running")
            .filter(sex="W")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class GentsGymProductListView(ListView):
    model = Product
    template_name = "products/gents_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="gym")
            .filter(sex="M")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class LadiesGymProductListView(ListView):
    model = Product
    template_name = "products/ladies_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="gym")
            .filter(sex="W")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class GentsOutdoorProductListView(ListView):
    model = Product
    template_name = "products/gents_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="outdoor")
            .filter(sex="M")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )


class LadiesOutdoorProductListView(ListView):
    model = Product
    template_name = "products/ladies_product_list.html"
    context_object_name = "products"
    # paginate_by = 10

    def get_queryset(self) -> QuerySet[Product]:
        return (
            Product.objects.filter(subcategory__name="outdoor")
            .filter(sex="W")
            .select_related("brand", "category", "subcategory")
            .order_by("name")
        )
