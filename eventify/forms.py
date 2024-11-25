from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": UsernameField}
