from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import EmailValidator

from .mixins import MixinsModel


# Create your models here.
class Company(MixinsModel):
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=30, unique=True, null=False)
    postal_code = models.PositiveIntegerField(
        validators=[MinValueValidator(10000), MaxValueValidator(99999)]
    )
    country = models.CharField(max_length=30, null=False)
    phone = models.PositiveIntegerField(
        validators=[MinValueValidator(100000000), MaxValueValidator(999999999)]
    )
    email = models.EmailField(validators=[EmailValidator()], unique=True)
    is_legal_address = models.BooleanField()

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Bank(MixinsModel):
    swift = models.CharField(max_length=6, unique=True, null=False)

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"


class BankAccount(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name="accounts")
    account_number = models.CharField(max_length=20, unique=True, null=False)
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="accounts"
    )

    class Meta:
        verbose_name = "Bank Account"
        verbose_name_plural = "Bank Accounts"
