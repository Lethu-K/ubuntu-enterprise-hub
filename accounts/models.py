from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = [
        ('customer', 'Customer'),
        ('entrepreneur', 'Entrepreneur'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"

class Service(models.Model):
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='services')
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100, default='General')
    price = models.IntegerField(default=100)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - R{self.price} by {self.agent.username}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
        ('completed', 'Completed'),
    ]
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_made')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings_received')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message = models.TextField(blank=True, help_text="e.g. Needed tomorrow 10am, 2 bedroom flat")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.title} - {self.client.username} -> {self.agent.username} ({self.status})"