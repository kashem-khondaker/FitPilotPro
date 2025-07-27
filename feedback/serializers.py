from rest_framework import serializers
from feedback.models import Feedback
from classes.models import FitnessClass

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'duration', 'instructor']
        ref_name = 'FeedbackFitnessClass'

from rest_framework import serializers
from .models import Feedback, FitnessClass
from .serializers import FitnessClassSerializer  # make sure this import path is correct

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    rating = serializers.IntegerField(min_value=1, max_value=5)
    fitness_class_details = FitnessClassSerializer(source='fitness_class', read_only=True)

    class Meta:
        model = Feedback
        fields = [
            'id',
            'user',
            'fitness_class',  # still needed internally
            'fitness_class_details',
            'rating',
            'comment',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['user', 'fitness_class_details', 'created_at', 'updated_at']
        extra_kwargs = {
            'fitness_class': {
                'write_only': True,  # Hide from Swagger GET response
                'required': False,   # Because it will come from context or view
            }
        }

    def to_representation(self, instance):
        """Hide 'fitness_class' from response"""
        rep = super().to_representation(instance)
        rep.pop('fitness_class', None)
        return rep

    def validate(self, attrs):
        user = self.context['request'].user
        fitness_class = attrs.get('fitness_class') or self.context.get('fitness_class')

        if not fitness_class:
            raise serializers.ValidationError("Fitness class is required.")

        # Optional: prevent duplicate feedback
        if self.instance is None and Feedback.objects.filter(user=user, fitness_class=fitness_class).exists():
            raise serializers.ValidationError("You have already submitted feedback for this class.")

        attrs['fitness_class'] = fitness_class
        return attrs


class FeedbackTestimonialSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    achievement = serializers.CharField(source="fitness_class.name", read_only=True)
    text = serializers.SerializerMethodField()
    
    class Meta:
        model = Feedback
        fields = ['id','name', 'image', 'achievement', 'text', 'rating' , 'created_at' ,'updated_at']
        read_only_fields = ["id","created_at" , "updated_at"]

    def get_name(self, obj):
        return obj.user.get_full_name() or obj.user.username if obj.user else "Anonymous"

    def get_image(self, obj):
        try:
            return obj.user.profile.image.url
        except:
            return "https://static.vecteezy.com/system/resources/previews/009/292/244/non_2x/default-avatar-icon-of-social-media-user-vector.jpg" or "https://i.pinimg.com/736x/82/85/96/828596ef925a10e8c1a76d3a3be1d3e5.jpg"

    def get_text(self, obj):
        return obj.comment or obj.fitness_class.description or ""
