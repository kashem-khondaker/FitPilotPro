from django.shortcuts import render
from rest_framework import viewsets, permissions
from memberships.models import MembershipPlan, Membership
from memberships.serializers import MembershipPlanSerializer, MembershipSerializer
from core.permissions import IsAdminOrStaff, IsMemberOrAdminStaff

# Create your views here.

class MembershipPlanViewSet(viewsets.ModelViewSet):
    queryset = MembershipPlan.objects.all()
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN':
            return MembershipPlan.objects.all()
        elif user.role == 'STAFF':
            return MembershipPlan.objects.all()
        return MembershipPlan.objects.none()

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.select_related('user', 'plan').all()
    serializer_class = MembershipSerializer
    permission_classes = [IsMemberOrAdminStaff]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Membership.objects.none()
        
        user = self.request.user
        if user.is_superuser or user.role == 'ADMIN':
            return Membership.objects.select_related('user', 'plan').all()
        elif user.role == 'STAFF':
            return Membership.objects.select_related('user', 'plan').all()
        elif user.role == 'MEMBER':
            return Membership.objects.filter(user=user).select_related('user', 'plan')
        return Membership.objects.none()

# inishial project download done
