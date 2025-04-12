from django.db import models
from django.contrib.auth.models import AbstractUser

# models.py

from django.db import models
from django.contrib.auth.models import User

class SavedRoute(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_routes')
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    start_lat = models.FloatField()
    start_lon = models.FloatField()
    end_lat = models.FloatField()
    end_lon = models.FloatField()
    transport_mode = models.CharField(max_length=50, choices=[
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('public_transport', 'Public Transport')
    ])
    saved_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.start_location} - {self.end_location} ({self.transport_mode})"


