from django.db import models
from accounts.models import CustomUser

# Create your models here.

class FitnessClass(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    duration = models.IntegerField()
    max_capacity = models.IntegerField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fitness_classes')
    schedule = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class ClassBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='class_bookings')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name}"
