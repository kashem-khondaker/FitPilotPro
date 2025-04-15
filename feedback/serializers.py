from rest_framework import serializers
from feedback.models import Feedback
from classes.models import FitnessClass

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'duration', 'instructor']
        ref_name = 'FeedbackFitnessClass'

class FeedbackSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer(read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'fitness_class', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']