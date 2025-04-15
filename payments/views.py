from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from payments.models import Payment
from payments.serializers import PaymentSerializer
from core.permissions import IsMemberOrAdminStaff, IsAdminOrStaff
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class PaymentPagination(PageNumberPagination):
    page_size = 15

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('user', 'membership', 'membership_plan').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsMemberOrAdminStaff]
    pagination_class = PaymentPagination

    def get_queryset(self):
        try:
            if getattr(self, 'swagger_fake_view', False):
                return Payment.objects.none()
            
            user = self.request.user
            if user.is_superuser or user.role == 'ADMIN':
                return Payment.objects.select_related('user', 'membership', 'membership_plan').all()
            elif user.role == 'STAFF':
                return Payment.objects.select_related('user', 'membership', 'membership_plan').all()
            elif user.role == 'MEMBER':
                return Payment.objects.filter(user=user).select_related('user', 'membership', 'membership_plan')
            return Payment.objects.none()
        except Exception as e:
            raise ValidationError({'error': str(e)})

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of payments",
        responses={
            200: PaymentSerializer(many=True),
            403: "Forbidden",
        },
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
            openapi.Parameter('amount_min', openapi.IN_QUERY, description="Minimum amount", type=openapi.TYPE_NUMBER),
            openapi.Parameter('amount_max', openapi.IN_QUERY, description="Maximum amount", type=openapi.TYPE_NUMBER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new payment",
        request_body=PaymentSerializer,
        responses={
            201: PaymentSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve details of a specific payment",
        responses={
            200: PaymentSerializer,
            404: "Not Found",
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update details of a specific payment",
        request_body=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update details of a specific payment",
        request_body=PaymentSerializer,
        responses={
            200: PaymentSerializer,
            400: "Bad Request",
            404: "Not Found",
        }
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a specific payment",
        responses={
            204: "No Content",
            404: "Not Found",
        }
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def payment_report(self, request):
        try:
            if request.user.role == 'ADMIN':
                payment_data = Payment.objects.select_related('user', 'membership_plan').all()
                # Serialize and return the data
                serializer = self.get_serializer(payment_data, many=True)
                return Response(serializer.data)
            return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
