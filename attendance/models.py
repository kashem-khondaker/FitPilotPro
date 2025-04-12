from django.db import models
from accounts.models import CustomUser
from classes.models import FitnessClass , ClassBooking

# Create your models here.

class Attendance(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='attendances')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='attendances')
    class_booking = models.ForeignKey(ClassBooking, on_delete=models.CASCADE, related_name='attendances')
    attendance_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name} - {self.attendance_date}"
