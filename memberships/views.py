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

class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.select_related('user', 'plan').all()
    serializer_class = MembershipSerializer
    permission_classes = [IsMemberOrAdminStaff]

# inishial project download done
