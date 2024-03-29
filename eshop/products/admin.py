from django.contrib import admin

from .models import (
    AttributeName,
    AttributeValue,
    Attribute,
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


@admin.register(AttributeValue)
class AttributeValueAdmin(admin.ModelAdmin):
    list_display = ("id", "value")


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "attribute_name", "attribute_value")
    list_filter = ("attribute_name", "attribute_value")


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "brand")
    list_filter = ("brand",)
    raw_id_fields = ("attributes",)
    search_fields = ("name",)


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = ("id", "code", "product", "price")
    list_filter = ("product",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")
    search_fields = ("name",)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product", "image")
    list_filter = ("product", "image")
    search_fields = ("name",)
