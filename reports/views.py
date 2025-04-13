from django.shortcuts import render
from rest_framework import viewsets, permissions
from reports.models import Report
from reports.serializers import ReportSerializer
from core.permissions import IsAdminOrStaff

# Create your views here.

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related('user', 'fitness_class').all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminOrStaff]
