from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    pass

class Event(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField()
    location = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.IntegerField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_fully_booked(self):
        return self.bookedevent_set.count() >= self.capacity


class BookedEvent(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('event', 'user')  # To ensure a user can book the same event only once

    def __str__(self):
        return f'{self.user.username} booked {self.event.name}'

