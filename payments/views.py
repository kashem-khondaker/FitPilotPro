from django.shortcuts import render
from rest_framework import viewsets, permissions
from payments.models import Payment
from payments.serializers import PaymentSerializer
from core.permissions import IsMemberOrAdminStaff

# Create your views here.

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('user', 'membership', 'membership_plan').all()
    serializer_class = PaymentSerializer
    permission_classes = [IsMemberOrAdminStaff]
