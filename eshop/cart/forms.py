from django import forms
from .models import CartItem


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ["quantity"]
        widgets = {"quantity": forms.NumberInput(attrs={"min": "1"})}
