from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth import get_user_model

from .models import Event


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)
        field_classes = {"username": UsernameField}


class EventCreateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'location', 'date', 'capacity']

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description'}),
            'location': forms.TextInput(attrs={'placeholder': 'Event Location'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Event Capacity'}),
        }