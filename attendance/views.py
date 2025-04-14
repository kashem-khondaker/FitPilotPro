from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from core.permissions import IsAdminOrStaff

# Create your views here.

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
    serializer_class = AttendanceSerializer
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Attendance.objects.none()
        
        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN':
            return Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
        elif user.role == 'STAFF':
            return Attendance.objects.select_related('user', 'fitness_class', 'class_booking').all()
        elif user.role == 'MEMBER':
            return Attendance.objects.filter(user=user).select_related('user', 'fitness_class', 'class_booking')
        return Attendance.objects.none()

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def attendance_report(self, request):
        if request.user.role == 'ADMIN':
            attendance_data = Attendance.objects.select_related('user', 'fitness_class').all()
            # Serialize and return the data
            serializer = self.get_serializer(attendance_data, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
