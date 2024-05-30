import io

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from django.core.files.base import ContentFile
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from .utils import generate_order_number, generate_invoice_number
from .mixins import TimeStampedModel
from products.utils import my_slugify_function
from products.models import Nomenclature


class ShippingAddress(models.Model):
    user = models.ForeignKey(
        User, related_name="shipping_addresses", on_delete=models.CASCADE
    )
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # def get_absolute_url(self):
    #     return reverse("orders:order_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.user.username} - {self.address}, {self.city}, {self.country}"

    class Meta:
        verbose_name = "Shipping Address"
        verbose_name_plural = "Shipping Addresses"


class Order(TimeStampedModel):

    STATUS_CHOICE = {
        "pending": "Pending",
        "completed": "Completed",
        "shipped": "Shipped",
        "delivered": "Delivered",
        "cancelled": "Cancelled",
    }  # key - actual value, value - human readable name

    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        ShippingAddress, related_name="orders", on_delete=models.CASCADE
    )
    code = models.CharField(max_length=10, default=generate_order_number, unique=True)
    status = models.CharField(max_length=9, choices=STATUS_CHOICE, default="pending")
    slug = AutoSlugField(populate_from="code", slugify_function=my_slugify_function)

    def __str__(self):
        return self.code

    def get_absolute_url(self):
        return reverse("orders:order_detail", kwargs={"slug": self.slug})

    def total_price(self):
        return sum([item.total_price() for item in self.items.all()])

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    nomenclature = models.ForeignKey(
        Nomenclature, on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveIntegerField()

    def total_price(self):
        return self.quantity * self.nomenclature.price

    def __str__(self):
        return f"Order Item of the order {self.order}: Nomenclature {self.nomenclature.code} - ({self.quantity} units)"

    class Meta:
        verbose_name = "Order Item"
        verbose_name_plural = "Order Items"


class Invoice(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="invoices")
    number = models.CharField(
        max_length=10, default=generate_invoice_number, unique=True
    )
    file = models.FileField(upload_to="invoices/", blank=True, null=True)

    def __str__(self):
        return self.number

    def generate_invoice_file(self):
        # Создаем буфер для хранения PDF
        buffer = io.BytesIO()

        # Создаем PDF-документ с ReportLab
        p = canvas.Canvas(buffer, pagesize=A4)
        p.drawString(100, 750, f"Invoice Number: {self.number}")
        p.drawString(100, 730, f"Order Code: {self.order.code}")
        p.drawString(
            100, 710, f"Order Date: {self.order.created_at.strftime('%Y-%m-%d')}"
        )

        # Добавьте сюда больше информации, как нужно
        p.showPage()
        p.save()

        # Получаем содержимое буфера
        pdf = buffer.getvalue()
        buffer.close()

        return ContentFile(pdf, f"invoice_{self.number}.pdf")

    def save(self, *args, **kwargs):
        if not self.file:
            self.file = self.generate_invoice_file()
        super().save(*args, **kwargs)
