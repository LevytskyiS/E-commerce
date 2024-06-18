from django.urls import path

from . import views


app_name = "products"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # Brands
    path("brands/", views.BrandListView.as_view(), name="brand_list"),
    path("brand/<slug:slug>/", views.BrandDetailView.as_view(), name="brand_detail"),
    # Product
    # ProductVariant
    path(
        "products/<slug:product_variant_slug>",
        views.ProductVariantDetailView.as_view(),
        name="product_variant",
    ),
    path(
        "product-variants/",
        views.ProductVariantListView.as_view(),
        name="product_variant_list",
    ),
    path(
        "category/<slug:slug>/<slug:product_slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
