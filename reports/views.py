from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from reports.models import Report
from reports.serializers import ReportSerializer
from core.permissions import IsAdminOrStaff
from memberships.models import Membership
from memberships.serializers import MembershipSerializer
from attendance.models import Attendance
from attendance.serializers import AttendanceSerializer
from feedback.models import Feedback
from feedback.serializers import FeedbackSerializer

# Create your views here.

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.select_related('user', 'fitness_class').all()
    serializer_class = ReportSerializer
    permission_classes = [IsAdminOrStaff]

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def membership_report(self, request):
        if request.user.role == 'ADMIN':
            # Generate membership report
            membership_data = Membership.objects.select_related('user', 'plan').all()
            serializer = MembershipSerializer(membership_data, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def attendance_report(self, request):
        if request.user.role == 'ADMIN':
            # Generate attendance report
            attendance_data = Attendance.objects.select_related('user', 'fitness_class').all()
            serializer = AttendanceSerializer(attendance_data, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    @action(detail=False, methods=['get'], permission_classes=[IsAdminOrStaff])
    def feedback_report(self, request):
        if request.user.role == 'ADMIN':
            # Generate feedback report
            feedback_data = Feedback.objects.select_related('user', 'fitness_class').all()
            serializer = FeedbackSerializer(feedback_data, many=True)
            return Response(serializer.data)
        return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
