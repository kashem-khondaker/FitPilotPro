from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer
from core.permissions import IsMemberOrAdminStaff
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'fitness_class').all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsMemberOrAdminStaff]

    def get_queryset(self):
        try:
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
        except Exception as e:
            raise ValidationError({'error': str(e)})
    
    @swagger_auto_schema(
        operation_description="Retrieve all feedback",
        responses={
            200: FeedbackSerializer(many= True),
            403:"Forbidden",
        }

    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new feedback",
        request_body=FeedbackSerializer,
        responses={
            201: FeedbackSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
