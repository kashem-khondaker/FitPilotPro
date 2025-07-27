from rest_framework import serializers
from feedback.models import Feedback
from classes.models import FitnessClass

class FitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'duration', 'instructor']
        ref_name = 'FeedbackFitnessClass'

class FeedbackSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    fitness_class = serializers.PrimaryKeyRelatedField(queryset=FitnessClass.objects.select_related('instructor').all() )
    rating = serializers.IntegerField(min_value=1, max_value=5)
    fitness_class_details = FitnessClassSerializer(source='fitness_class', read_only=True)

    class Meta:
        model = Feedback
        fields = ['id', 'user', 'fitness_class', 'fitness_class_details', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user', 'created_at', 'updated_at']

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
