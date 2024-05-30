from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse

from .mixins import AttributesBase, NameSlugModel


class AttributeName(AttributesBase):
    class Meta:
        verbose_name = "Attribute Name"
        verbose_name_plural = "Attribute Names"


class AttributeValue(models.Model):
    value = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = "Attribute Value"
        verbose_name_plural = "Attribute Values"


class Attribute(models.Model):
    attribute_name = models.ForeignKey(
        AttributeName, related_name="attribute", on_delete=models.CASCADE
    )
    attribute_value = models.ForeignKey(
        AttributeValue, related_name="attribute", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.attribute_name} - {self.attribute_value}"

    class Meta:
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"


class Category(NameSlugModel):
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class Subcategory(NameSlugModel):
    category = models.ManyToManyField(
        Category,
        related_name="subcategory",
    )

    class Meta:
        verbose_name = "Subcategory"
        verbose_name_plural = "Subcategories"


class Brand(NameSlugModel):
    subcategory = models.ManyToManyField(
        Subcategory,
        related_name="brand",
    )
    category = models.ManyToManyField(Category, related_name="brand")

    def get_products(self):
        return self.product.all()

    def get_absolute_url(self):
        return reverse("products:brand_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Product(NameSlugModel):
    sex = models.CharField(max_length=1, choices=(("M", "Men"), ("W", "Women")))
    brand = models.ForeignKey(Brand, related_name="product", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE
    )
    subcategory = models.ForeignKey(
        Subcategory, related_name="product", on_delete=models.CASCADE
    )
    attributes = models.ManyToManyField(Attribute, related_name="products")

    def get_nomenclatures(self):
        return self.nomenclatures.all()

    def get_absolute_url(self):
        return reverse(
            "products:product_detail",
            kwargs={"slug": self.brand.slug, "product_slug": self.slug},
        )

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"


class Nomenclature(models.Model):
    code = models.CharField(max_length=15, unique=True)
    product = models.ForeignKey(
        Product, related_name="nomenclatures", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0, "The price must be equal or greater than 0.")],
    )
    quantity_available = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.code

    class Meta:
        verbose_name = "Nomenclature"
        verbose_name_plural = "Nomenclatures"


class Image(models.Model):
    name = models.CharField(max_length=256)
    image = models.URLField(unique=True)

    def __str__(self):
        if self.name:
            return self.name
        return self.image

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"


class ProductImage(models.Model):
    name = models.CharField(max_length=256)
    product = models.ForeignKey(
        Product, related_name="product_image", on_delete=models.CASCADE
    )
    image = models.ForeignKey(
        Image, related_name="product_image", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Product Image of {self.product}"

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"
