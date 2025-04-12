from rest_framework import serializers
from payments.models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'membership', 'membership_plan', 'amount', 'payment_date', 'payment_method', 'transaction_id']
        read_only_fields = [ 'user', 'payment_date']