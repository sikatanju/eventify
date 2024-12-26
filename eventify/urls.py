from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView

from . import views


urlpatterns = [
    path('', views.landing_page, name='landing_page'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'), 
    path('signup/', views.SignupView.as_view(), name='signup'),
    
    path('events/', views.event_home, name='event_home'),
    path('events/create', views.event_create, name='event_create'),
    path('events/update/<int:pk>', views.event_update, name='event_update'),

    path('events/booked', views.event_booked_mine, name='event_booked'),
    path('events/manage', views.event_manage, name='event_manage'),


    path('events/book/<int:pk>', views.book_event, name='book_event'),
]
