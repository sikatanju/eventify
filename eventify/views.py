from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.views import LoginView, LogoutView

from .models import Event

from .forms import CustomUserCreationForm
# Create your views here.

def landing_page(request):
    return render(request, 'base/landing.html')


def event_home(request):
    events = Event.objects.all()
    return render(request, 'events_home.html', {'events': events})
    pass
    return HttpResponse ("Event Home")


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')