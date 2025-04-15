from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError
from memberships.models import MembershipPlan, Membership
from memberships.serializers import MembershipPlanSerializer, MembershipSerializer
from core.permissions import IsAdminOrStaff, IsMemberOrAdminStaff
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAdminOrStaff]

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
        operation_description="Retrieve all membership plans",
        responses={
            200: MembershipPlanSerializer(many=True),
            403: "Forbidden",
        }
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
   