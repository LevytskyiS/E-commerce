from typing import Any, Mapping
from django.core.files.base import File
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.utils import ErrorList

from .models import ShippingAddress


class CreateShippingAddressForm(ModelForm):

    class Meta:
        model = ShippingAddress
        exclude = ["user"]
