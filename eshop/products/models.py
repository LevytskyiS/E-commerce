from django.db import models
from django.core.validators import MinValueValidator
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField

from .utils import my_slugify_function


class AttributeName(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name


class AttributeValue(models.Model):
    value = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.value


class Attribute(models.Model):
    attribute_name = models.ForeignKey(
        AttributeName, related_name="attribute", on_delete=models.CASCADE
    )
    attribute_value = models.ForeignKey(
        AttributeValue, related_name="attribute", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.attribute_name} - {self.attribute_value}"


class Category(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(populate_from="name", slugify_function=my_slugify_function)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(populate_from="name", slugify_function=my_slugify_function)
    category = models.ManyToManyField(
        Category,
        related_name="subcategory",
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(populate_from="name", slugify_function=my_slugify_function)
    subcategory = models.ManyToManyField(
        Subcategory,
        related_name="brand",
    )
    category = models.ManyToManyField(Category, related_name="brand")

    def get_products(self):
        return self.product.all()

    def get_absolute_url(self):
        return reverse("products:brand_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    slug = AutoSlugField(populate_from="name", slugify_function=my_slugify_function)
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

    def __str__(self):
        return self.name


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


class Image(models.Model):
    name = models.CharField(max_length=256)
    image = models.URLField(unique=True)

    def __str__(self):
        if self.name:
            return self.name
        return self.image


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
