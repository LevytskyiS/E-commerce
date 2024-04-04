from django.urls import path

from . import views


app_name = "products"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # Brands
    path("brands/", views.BrandListView.as_view(), name="brand_list"),
    path("brands/<int:pk>", views.BrandDetailView.as_view(), name="brand_detail"),
    # Product
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path(
        "gents-products/",
        views.GentsProductListView.as_view(),
        name="gents_product_list",
    ),
    path(
        "ladies-products/",
        views.LadiesProductListView.as_view(),
        name="ladies_product_list",
    ),
    path(
        "gents-hiking-products/",
        views.GentsHikingProductListView.as_view(),
        name="gents_hiking_product_list",
    ),
    path(
        "ladies-hiking-products/",
        views.LadiesHikingProductListView.as_view(),
        name="ladies_hiking_product_list",
    ),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
]
