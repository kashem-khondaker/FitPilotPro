from rest_framework import serializers
from attendance.models import Attendance
from classes.serializers import FitnessClassSerializer, ClassBookingSerializer

class AttendanceSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)
    class_booking = ClassBookingSerializer(read_only=True)

    class Meta:
        model = Attendance
        fields = ['id', 'user', 'fitness_class', 'class_booking', 'attendance_date']