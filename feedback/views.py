from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer
from core.permissions import IsMemberOrAdminStaff
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from core.permissions import FeedbackPermission

# Create your views here.

class FeedbackPagination(PageNumberPagination):
    page_size = 8

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.select_related('user', 'fitness_class').all()
    serializer_class = FeedbackSerializer
    permission_classes = [FeedbackPermission]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['rating', 'fitness_class__name']
    search_fields = ['comment', 'fitness_class__name', 'user__email']
    ordering_fields = ['rating', 'created_at']
    pagination_class = FeedbackPagination

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
        operation_description="Retrieve a paginated list of feedback",
        responses={
            200: FeedbackSerializer(many=True),
            403: "Forbidden",
        },
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        ]
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
