from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from memberships.models import MembershipPlan, Membership
from memberships.serializers import MembershipPlanSerializer, MembershipSerializer
from core.permissions import IsAdminOrStaff, IsMemberOrAdminStaff
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

# Create your views here.

class MembershipPlanPagination(PageNumberPagination):
    page_size = 10

class MembershipPagination(PageNumberPagination):
    page_size = 5

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAdminOrStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['price', 'duration_in_days']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'duration_in_days']
    pagination_class = MembershipPlanPagination

    def get_queryset(self):
        try:
            user = self.request.user
            if not user.is_authenticated:
                return MembershipPlan.objects.none()

            if user.is_superuser or user.role == 'ADMIN':
                return MembershipPlan.objects.all()
            elif user.role == 'STAFF':
                return MembershipPlan.objects.all()
            return MembershipPlan.objects.none()
        except Exception as e:
            raise ValidationError({'error': str(e)})

    @swagger_auto_schema(
        operation_description="Retrieve a paginated list of membership plans",
        responses={
            200: MembershipPlanSerializer(many=True),
            403: "Forbidden",
        },
        manual_parameters=[
            openapi.Parameter('page', openapi.IN_QUERY, description="Page number", type=openapi.TYPE_INTEGER),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new membership plan",
        request_body=MembershipPlanSerializer,
        responses={
            201: MembershipPlanSerializer,
            400: "Bad Request",
        }
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.select_related('user', 'plan').all()
    serializer_class = MembershipSerializer
    permission_classes = [IsMemberOrAdminStaff]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['is_active', 'plan__name']
    search_fields = ['user__email', 'plan__name']
    ordering_fields = ['start_date', 'end_date']
    pagination_class = MembershipPagination

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Membership.objects.none()

        user = self.request.user
        if not user.is_authenticated:
            return Membership.objects.none()

        if user.is_superuser or user.role == 'ADMIN':
            return Membership.objects.select_related('user', 'plan').all()
        elif user.role == 'STAFF':
            return Membership.objects.select_related('user', 'plan').all()
        elif user.role == 'MEMBER':
            return Membership.objects.filter(user=user).select_related('user', 'plan')
        return Membership.objects.none()

# inishial project download done
