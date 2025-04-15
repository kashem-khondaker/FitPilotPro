from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from classes.models import FitnessClass, ClassBooking
from classes.serializers import FitnessClassSerializer, ClassBookingSerializer
from core.permissions import IsAdminOrStaffOrReadOnly
from drf_yasg.utils import swagger_auto_schema
# Create your views here.

class FitnessClassViewSet(viewsets.ModelViewSet):
    queryset = FitnessClass.objects.select_related('instructor').all()
    serializer_class = FitnessClassSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]

    def get_queryset(self):
        # Handle Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return FitnessClass.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return FitnessClass.objects.select_related('instructor').all()

        if user.is_superuser or user.role == 'ADMIN':
            return FitnessClass.objects.select_related('instructor').all()
        elif user.role == 'STAFF':
            return FitnessClass.objects.select_related('instructor').all()
        
        return FitnessClass.objects.select_related('instructor').all()
    
    @swagger_auto_schema(
        operation_description="Retrieve all fitness classes",
        responses={
            200: FitnessClassSerializer(many=True),
            403: "Forbidden",
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new fitness class",
        request_body= FitnessClassSerializer,
        responses={
            201: FitnessClassSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

class ClassBookingViewSet(viewsets.ModelViewSet):
    
    serializer_class = ClassBookingSerializer
    permission_classes = [IsAdminOrStaffOrReadOnly]

    def get_queryset(self):
        user = self.request.user

        if getattr(self, 'swagger_fake_view', False):
            return ClassBooking.objects.none()
        
        if user.is_superuser or user.role == 'ADMIN':
            return ClassBooking.objects.select_related('user', 'fitness_class').all()
        elif user.role == 'STAFF':
            return ClassBooking.objects.select_related('user', 'fitness_class').all()
        elif user.role == 'MEMBER':
            return ClassBooking.objects.filter(user=user).select_related('user', 'fitness_class')
        
        return ClassBooking.objects.none()


    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)

# 017 92 15 77 12