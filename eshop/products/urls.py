from django.urls import path

from . import views


app_name = "products"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    # Category
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    # Subategory
    path(
        "subcategories/", views.SubcategoryListView.as_view(), name="subcategory_list"
    ),
    # Brands
    path("brands/", views.BrandListView.as_view(), name="brand_list"),
    path("brands/<int:pk>", views.BrandDetailView.as_view(), name="brand_detail"),
    # Product
    path("products/", views.ProductListView.as_view(), name="product_list"),
    path("products/<int:pk>", views.ProductDetailView.as_view(), name="product_detail"),
]
