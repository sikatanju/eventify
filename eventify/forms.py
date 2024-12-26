from django import forms

from django.utils import timezone
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


class EventUpdateForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'date', 'capacity']
        exclude = ['location']  # Exclude location field from being shown in the form

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Event Name'}),
            'description': forms.Textarea(attrs={'placeholder': 'Event Description'}),
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'placeholder': 'YYYY-MM-DDTHH:MM'}),
            'capacity': forms.NumberInput(attrs={'placeholder': 'Event Capacity'}),
        }

    def clean_date(self):
        date = self.cleaned_data.get('date')
        if self.instance and self.instance.date < timezone.now():
            if date != self.instance.date:
                raise forms.ValidationError("You cannot change the date of an event that has already passed.")
        return date

    def clean_capacity(self):
        capacity = self.cleaned_data.get('capacity')
        if self.instance and capacity < self.instance.current_booked:
            raise forms.ValidationError("Capacity cannot be set lower than the number of currently booked users.")
        return capacity