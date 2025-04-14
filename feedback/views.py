from django.shortcuts import render
from rest_framework import viewsets, permissions
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer
from core.permissions import IsMemberOrAdminStaff

# Create your views here.

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'fitness_class').all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsMemberOrAdminStaff]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Feedback.objects.none()

        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN':
            return Feedback.objects.select_related('user', 'fitness_class').all()
        elif user.role == 'STAFF':
            return Feedback.objects.filter(fitness_class__instructor=user).select_related('user', 'fitness_class')
        elif user.role == 'MEMBER':
            return Feedback.objects.filter(user=user).select_related('user', 'fitness_class')
        return Feedback.objects.none()
