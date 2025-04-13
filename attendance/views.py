from django.shortcuts import render
from rest_framework import viewsets, permissions
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from core.permissions import IsAdminOrStaff

# Create your views here.

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrStaff]
