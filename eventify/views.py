from django.shortcuts import render

from django.urls import reverse
from django.shortcuts import redirect
from django.views import generic
# from django.contrib.auth.views import LoginView, LogoutView

from .models import Event

from .forms import CustomUserCreationForm, EventCreateForm
# Create your views here.

def landing_page(request):
    return render(request, 'base/landing.html')


def event_home(request):
    events = Event.objects.all()
    return render(request, 'event_home.html', {'events': events})


def event_create(request):
    current_user = request.user
    print(current_user.is_superuser)

    if not current_user.is_superuser:
        return render(request, 'permission_denied.html')
    else:
        event_form = EventCreateForm()
        
        if request.method == 'POST':
            event_form = EventCreateForm(data=request.POST)
            if event_form.is_valid():
                event = event_form.save(commit=False)
                event.organizer = current_user
                event.save()
                return redirect('event_home')
    
        return render(request, 'event_create.html', {'event_form': event_form, 'user': current_user})
    

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')