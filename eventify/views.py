from django.shortcuts import render

from django.urls import reverse
from django.shortcuts import redirect
from django.views import generic
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.views import LoginView, LogoutView

from .models import Event, BookedEvent

from .forms import CustomUserCreationForm, EventCreateForm


def landing_page(request):
    return render(request, 'base/landing.html')


def event_home(request):
    current_user = request.user
    events = Event.objects.all()
    print(current_user)
    print(current_user.is_superuser)
    if str(current_user) == 'AnonymousUser':
        return render(request, 'event_home.html', {'events': events})
    
    if not request.user.is_superuser:
        booked_event_ids = set(Event.objects.filter(bookings__user=request.user).values_list('id', flat=True))
        for id in booked_event_ids:
            print(id)
        return render(request, 'event_home.html', {'events': events, 'booked_ids': booked_event_ids})


    return render(request, 'event_home.html', {'events': events})

@login_required
def event_booked_mine(request):
    if not request.user.is_superuser:
        events = Event.objects.filter(bookings__user=request.user)
        return render(request, 'event_booked_mine.html', {'events': events})
    else:
        return render(request, 'permission_denied.html')
    

@login_required
def event_manage(request):
    if request.user.is_superuser:
        events = Event.objects.filter(organizer=request.user)
        return render(request, 'event_manage.html', {'events': events})
    else:
        return render(request, 'permission_denied.html')
    

@login_required
def event_create(request):
    current_user = request.user

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
    

@login_required
def book_event(request, pk):
    if not request.user.is_superuser:
        try:
            event = Event.objects.get(pk=pk)
            if event.is_fully_booked:
                return render(request, 'event_fully_booked.html')

            if BookedEvent.objects.filter(user=request.user, event=event).exists():
                return render(request, 'event_already_booked.html')

            booking = BookedEvent.objects.create(user=request.user, event=event)
            return redirect('event_home')

        except Event.DoesNotExist:
            return render(request, 'event_not_found.html')
    else:
        return render(request, "organizer_permission_denied.html")

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self) -> str:
        return reverse('login')