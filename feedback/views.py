from django.shortcuts import render
from rest_framework import viewsets, permissions
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer

# Create your views here.

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'fitness_class').all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]
