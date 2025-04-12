from rest_framework import serializers
from reports.models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'user', 'fitness_class', 'report_date', 'content']
        read_only_fields = ['user', 'report_date']