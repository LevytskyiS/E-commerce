from django.contrib import admin

from .models import (
    AttributeName,
    AttributeValue,
    AttributeImage,
    Attribute,
    Category,
    Subcategory,
    Brand,
    Product,
    ProductVariant,
    Nomenclature,
    Image,
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


@admin.register(AttributeImage)
class AttributeImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image")
    search_fields = ("name",)
    list_filter = ("name",)
    ordering = ("id",)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("id", "attribute_name", "attribute_value", "attribute_image")
    list_filter = ("attribute_name", "attribute_value", "attribute_image")


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


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product", "attributes")
    list_filter = ("product",)
    search_fields = ("name",)


@admin.register(Nomenclature)
class NomenclatureAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "quantity_available",
        "price",
        "product_variant",
        "attributes",
    )
    list_filter = ("product_variant",)
    search_fields = ("nomeclature",)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "image", "product_variant")
    search_fields = ("name",)
