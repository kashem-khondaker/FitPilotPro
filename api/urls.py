from django.urls import path, include
from rest_framework.routers import DefaultRouter 
from rest_framework_nested import routers  
from classes.views import FitnessClassViewSet, ClassBookingViewSet
from memberships.views import MembershipPlanViewSet, MembershipViewSet
from payments.views import PaymentViewSet
from feedback.views import FeedbackViewSet
from attendance.views import AttendanceViewSet
from reports.views import ReportViewSet
from accounts.views import UserProfileView, UserAccountView

router = DefaultRouter()

router.register(r'accounts', UserAccountView, basename="accounts")
router.register(r'users/profile', UserProfileView, basename='userprofile')
router.register(r'fitness_classes', FitnessClassViewSet, basename='fitnessclass')  
router.register(r'class_bookings', ClassBookingViewSet, basename='classbooking')
router.register(r'membership_plans', MembershipPlanViewSet, basename='membershipplan')
router.register(r'memberships', MembershipViewSet, basename='membership')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')
router.register(r'attendances', AttendanceViewSet, basename='attendance')


fitness_classes_router = routers.NestedSimpleRouter(
    router, 
    r'fitness_classes',  
    lookup='fitness_class'  
)
fitness_classes_router.register(
    r'feedbacks', 
    FeedbackViewSet, 
    basename='class-feedbacks'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(fitness_classes_router.urls)),  
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]