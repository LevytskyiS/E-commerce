from django.core.cache import cache
from django.db.models import Prefetch
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import (
    ListView,
    DetailView,
)

from .models import (
    Brand,
    Product,
    Attribute,
    ProductVariant,
    Nomenclature,
    Category,
    Subcategory,
)

from cart.models import Cart, CartItem


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

    def get_queryset(self) -> QuerySet[Brand]:
        return Brand.objects.order_by("name")


# Product
class ProductDetailView(DetailView):
    model = Product
    slug_url_kwarg = "product_slug"
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_queryset(self):
        product = Product.objects.select_related(
            "brand", "category", "subcategory"
        ).prefetch_related(
            "attributes__attribute_name",
            "attributes__attribute_value",
        )

        return product


# ProductVariant
class ProductVariantDetailView(DetailView):
    model = ProductVariant
    slug_url_kwarg = "product_variant_slug"
    template_name = "products/product_variant_detail.html"
    context_object_name = "product_variant"

    def post(self, request, *args, **kwargs):
        nomenclature_code = request.POST.get("nomenclature_code")
        nomenclature = get_object_or_404(Nomenclature, code=nomenclature_code)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart, nomenclature=nomenclature
        )

        if not created:
            cart_item.quantity += 1
        cart_item.save()

        redirect_url = self.get_object().get_absolute_url()
        return redirect(redirect_url)

    def get_queryset(self):
        product_variant = ProductVariant.objects.select_related(
            "product",
            "product__brand",
            "product__subcategory",
            "product__category",
            "attributes__attribute_name",
            "attributes__attribute_value",
        ).prefetch_related(
            "product__attributes__attribute_name",
            "product__attributes__attribute_value",
        )

        color = self.request.GET.get("color")

        if color:
            product_variant = product_variant.filter(
                attributes__attribute_value__value=color
            )
        return product_variant


class ProductVariantListView(ListView):
    model = ProductVariant
    template_name = "products/product_variant_list.html"
    context_object_name = "product_variants"

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

        properties = Attribute.objects.filter(
            attribute_name__name="properties"
        ).select_related("attribute_value")

        categories = Category.objects.all()
        subcategories = Subcategory.objects.all().prefetch_related("category")
        brands = Brand.objects.all()

        context["categories"] = categories
        context["subcategories"] = subcategories
        context["brands"] = brands
        context["colors"] = colors
        context["properties"] = properties

        context["selected_categories"] = self.request.GET.getlist("category")
        context["selected_subcategories"] = self.request.GET.getlist("subcategory")
        context["selected_brands"] = self.request.GET.getlist("brand")
        context["selected_colors"] = self.request.GET.getlist("color")
        context["selected_properties"] = self.request.GET.getlist("property")

        return context

    def get_queryset(self) -> QuerySet[Product]:
        queryset = ProductVariant.objects.all().select_related("product")
        queryset = queryset.prefetch_related(
            Prefetch(
                "attributes",
                queryset=Attribute.objects.select_related(
                    "attribute_name", "attribute_value"
                ),
            ),
            Prefetch(
                "product",
                queryset=Product.objects.select_related(
                    "brand", "category", "subcategory"
                ),
            ),
        )

        categories = self.request.GET.getlist("category")
        subcategories = self.request.GET.getlist("subcategory")
        brands = self.request.GET.getlist("brand")
        properties = self.request.GET.getlist("property")
        colors = self.request.GET.getlist("color")

        if categories:
            queryset = queryset.filter(product__category__name__in=categories)

        if subcategories:
            queryset = queryset.filter(product__subcategory__name__in=subcategories)

        if brands:
            queryset = queryset.filter(product__brand__name__in=brands)

        if properties:
            queryset = queryset.filter(
                product__attributes__attribute_value__value__in=properties,
            )

        if colors:
            queryset = queryset.filter(
                attributes__attribute_value__value__in=colors,
            ).distinct()

        return queryset
