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
    # Gents
    path(
        "gents-products/",
        views.GentsProductListView.as_view(),
        name="gents_product_list",
    ),
    # Ladies
    path(
        "ladies-products/",
        views.LadiesProductListView.as_view(),
        name="ladies_product_list",
    ),
    # Hiking
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
    # Running
    path(
        "gents-running-products/",
        views.GentsRunningProductListView.as_view(),
        name="gents_running_product_list",
    ),
    path(
        "ladies-running-products/",
        views.LadiesRunningProductListView.as_view(),
        name="ladies_running_product_list",
    ),
    # Gym
    path(
        "gents-gym-products/",
        views.GentsGymProductListView.as_view(),
        name="gents_gym_product_list",
    ),
    path(
        "ladies-gym-products/",
        views.LadiesGymProductListView.as_view(),
        name="ladies_gym_product_list",
    ),
    # Outdoor
    path(
        "gents-outdoor-products/",
        views.GentsOutdoorProductListView.as_view(),
        name="gents_outdoor_product_list",
    ),
    path(
        "ladies-outdoor-products/",
        views.LadiesOutdoorProductListView.as_view(),
        name="ladies_outdoor_product_list",
    ),
    path(
        "<slug:slug>/<slug:product_slug>/",
        views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]
