from django.contrib import admin

from .models import (
    AttributeName,
    AttributeValue,
    Attribute,
    Category,
    Subcategory,
    Brand,
    Product,
    Nomenclature,
    Image,
    ProductImage,
)


@admin.register(AttributeName)
class AttributeNameAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("id",)


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", "value")
    search_fields = ("value",)
    list_filter = ("value",)
    ordering = ("id",)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "attribute_name", "attribute_value")
    list_filter = ("attribute_name", "attribute_value")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
    )
    list_filter = ("category",)
    raw_id_fields = ("category",)
    search_fields = ("name",)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    raw_id_fields = ("subcategory", "category")
    list_filter = (
        "category",
        "subcategory",
    )
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "sex", "brand", "category", "subcategory")
    list_filter = ("brand", "category", "subcategory")
    raw_id_fields = ("attributes",)
    search_fields = ("name",)


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "quantity_available", "price", "product")
    list_filter = ("product",)
    search_fields = ("nomeclature",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")
    search_fields = ("name",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product", "image")
    list_filter = ("product", "image")
    search_fields = ("name",)
    raw_id_fields = ("product",)
