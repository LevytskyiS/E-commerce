from typing import Any
from django.forms import (
    ModelForm,
    CharField,
    EmailField,
    EmailInput,
    TextInput,
    PasswordInput,
    ModelChoiceField,
    ValidationError,
)

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegisterUserForm(UserCreationForm):
    first_name = CharField(label="First Name", widget=TextInput())
    last_name = CharField(label="Last Name", widget=TextInput())
    username = CharField(label="Login", widget=TextInput())
    email = EmailField(label="Email", widget=EmailInput())
    password1 = CharField(label="Password", widget=PasswordInput())
    password2 = CharField(
        label="Password confirmation",
        widget=PasswordInput(),
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )


class LoginUserForm(AuthenticationForm):
    username = CharField(label="Login", widget=TextInput())
    password = CharField(label="Password", widget=PasswordInput())


class UserUpdateFrom(ModelForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    first_name = CharField(max_length=50, required=True)
    last_name = CharField(max_length=50, required=True)
