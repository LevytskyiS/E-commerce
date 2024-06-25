from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm, CharField, BooleanField
from django.forms.utils import ErrorList

from .models import ShippingAddress


class CreateShippingAddressForm(ModelForm):

    class Meta:
        model = ShippingAddress
        exclude = ["user", "is_default", "is_active"]

    address = CharField(max_length=100, required=True)
    city = CharField(max_length=100, required=True)
    country = CharField(max_length=100, required=True)
    postal_code = CharField(max_length=20, required=True)


class UpdateShippingAddressForm(ModelForm):

    class Meta:
        model = ShippingAddress
        exclude = ["user", "is_default"]

    address = CharField(max_length=100, required=True)
    city = CharField(max_length=100, required=True)
    country = CharField(max_length=100, required=True)
    postal_code = CharField(max_length=20, required=True)
    is_active = BooleanField(required=True)
