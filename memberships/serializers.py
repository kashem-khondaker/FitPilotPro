from rest_framework import serializers
from memberships.models import MembershipPlan, Membership

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = ['id', 'name', 'description', 'price', 'duration_in_days', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Membership
        fields = ['id', 'user', 'plan', 'start_date', 'end_date', 'is_active']
        read_only_fields = [ 'user', 'start_date']