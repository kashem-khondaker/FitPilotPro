from rest_framework import serializers
from attendance.models import Attendance

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'user', 'fitness_class', 'class_booking', 'attendance_date']
        read_only_fields = [ 'user', 'attendance_date']