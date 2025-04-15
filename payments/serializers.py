from rest_framework import serializers
from payments.models import Payment
from memberships.models import  MembershipPlan
from memberships.serializers import MembershipPlanSerializer


class SimpleMembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = [ 'name', 'description', 'price', 'duration_in_days']

class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    membership_plan = SimpleMembershipPlanSerializer(read_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'user', 'membership', 'membership_plan', 'amount', 'payment_date', 'payment_method', 'transaction_id']
        # read_only_fields = [ 'user', 'payment_date']