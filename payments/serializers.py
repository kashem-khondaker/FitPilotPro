from rest_framework import serializers
from payments.models import Payment
from memberships.serializers import MembershipSerializer, MembershipPlanSerializer

class PaymentSerializer(serializers.ModelSerializer):
    membership = MembershipSerializer(read_only=True)
    membership_plan = MembershipPlanSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'membership', 'membership_plan', 'amount', 'payment_date', 'payment_method', 'transaction_id']
        read_only_fields = [ 'user', 'payment_date']