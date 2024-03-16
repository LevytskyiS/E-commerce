from django.contrib import admin

from .models import (
    AttributeName,
    AttributeValue,
    Attribute,
    # Category,
    Brand,
    # Subcategory,
    Product,
    Image,
    ProductImage,
)


@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", "value")


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "attribute_name", "attribute_value")
    list_filter = ("attribute_name", "attribute_value")


# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "name")
#     search_fields = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


# @admin.register(Subcategory)
# class SubcategoryAdmin(admin.ModelAdmin):
#     list_display = ("id", "name", "category")
#     list_filter = ("category",)
#     raw_id_fields = ("brand",)
#     search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand", "price")
    list_filter = ("brand",)
    search_fields = ("name",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")
    search_fields = ("name",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product", "image")
    list_filter = ("product", "image")
    search_fields = ("name",)
