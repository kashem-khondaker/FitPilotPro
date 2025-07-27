from django.db import models
from django.core.exceptions import ValidationError
from accounts.models import CustomUser
from cloudinary.models import CloudinaryField

# Create your models here.

class FitnessClass(models.Model):
    LEVEL_CHOICE = (
        ('BEGINNER','Beginner'),
        ('INTERMEDIATE','Intermediate'),
        ('ALL LEVELS' , 'All levels'),
        ('ADVANCED' , 'Advanced'),
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = CloudinaryField('Class_Image', null=True, blank=True)
    duration = models.IntegerField()
    max_capacity = models.IntegerField()
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fitness_classes')
    schedule = models.DateTimeField()
    level = models.CharField(max_length=100 , choices=LEVEL_CHOICE , default='BEGINNER')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    old_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def is_fully_booked(self):
        return self.bookings.count() >= self.max_capacity

    def clean(self):
        super().clean()
        if self.max_capacity <= 0:
            raise ValidationError("Max capacity must be a positive integer.")

class ClassSchedule(models.Model):
    DAY_CHOICE = (
        ('MONDAY', 'Monday'),
        ('TUESDAY', 'Tuesday'),
        ('WEDNESDAY', 'Wednesday'),
        ('THURSDAY', 'Thursday'),
        ('FRIDAY', 'Friday'),
        ('SATURDAY', 'Saturday'),
        ('SUNDAY', 'Sunday'),
    )
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='schedules')
    day = models.CharField(max_length=20 , choices=DAY_CHOICE , default='SUNDAY')  # e.g. "Monday"
    time = models.TimeField(max_length=50)  # e.g. "6:00 PM - 6:45 PM"
    instructor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



class ClassBooking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='class_bookings')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'fitness_class')

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name}"

    def clean(self):
        super().clean()
        if self.fitness_class.is_fully_booked():
            raise ValidationError("This class is fully booked.")
