from django.db import models
from django.core.validators import MinValueValidator


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


# class Category(models.Model):
#     name = models.CharField(max_length=30, unique=True)

#     def __str__(self):
#         return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30, unique=True)

    def __str__(self):
        return self.name


# class Subcategory(models.Model):
#     name = models.CharField(max_length=30, unique=True)
#     category = models.ForeignKey(
#         Category,
#         related_name="subcategory",
#         on_delete=models.CASCADE,
#     )
#     brand = models.ManyToManyField(
#         Brand,
#         related_name="subcategory",
#     )

#     def __str__(self):
#         return self.name


class Product(models.Model):
    name = models.CharField(max_length=30, unique=True)
    brand = models.ForeignKey(Brand, related_name="product", on_delete=models.CASCADE)
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(0, "The price must be equal or greater than 0.")],
    )
    attributes = models.ManyToManyField(Attribute, related_name="products")

    def __str__(self):
        return self.name


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
