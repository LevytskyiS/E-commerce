from django.urls import path

from . import views


app_name = "products"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # Brands
    path("brands/", views.BrandListView.as_view(), name="brand_list"),
    path("brands/<int:pk>", views.BrandDetailView.as_view(), name="brand_detail"),
]
