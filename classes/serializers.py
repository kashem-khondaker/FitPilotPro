from rest_framework import serializers
from classes.models import FitnessClass, ClassBooking ,ClassSchedule
from accounts.models import CustomUser 
from accounts.serializers import ProfileSerializer

class InstructorSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email' , 'profile']


class ClassScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClassSchedule
        fields = ['id', 'day', 'time']

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor = InstructorSerializer(read_only=True)
    instructor_id = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(), source='instructor', write_only=True
    )
    image = serializers.SerializerMethodField()
    schedules = ClassScheduleSerializer(many=True, read_only=True)

    class Meta:
        model = FitnessClass
        fields = [
            'id', 'name', 'description', 'image', 'duration', 'max_capacity',
            'instructor', 'instructor_id', 'schedule',  'level',
            'price', 'old_price', 'schedules',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

    def get_image(self, obj):
        if obj.image:
            return obj.image.url
        return None

class ClassBookingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.all())

    class Meta:
        model = ClassBooking
        fields = ['id', 'user', 'fitness_class', 'booking_date']
        read_only_fields = ['booking_date']
