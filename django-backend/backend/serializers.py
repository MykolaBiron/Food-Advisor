from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Meal, Image, Profile, WeightEntry

class ImageSerializer(serializers.Serializer):
    class Meta:
        model = Image
        fields = []


class MealSerializer(serializers.Serializer):
    "Serializer for the Meal model"
    class Meta:
        model = Meal
        fields = ['user', 'image', 'date', 'name', 
                  'saved', 'total_calories', 'total_proteins']
        
        
class WeightEntrySerializer(serializers.Serializer):
    class Meta:
        model = WeightEntry
        fields = ['profile', 'weight', 'date_updated']

class ProfileSerializer(serializers.Serializer):
    class Meta:
        model = Profile
        fields = ['user', 'age', 'sex', 'height', 'weight',
                  'goal', 'activity']
        

class CreateProfileSerializer(serializers.Serializer):
    """Serializer to create Profile based on user input"""
    height = serializers.IntegerField(min_value=50, max_value=230)
    weight = serializers.FloatField(min_value=5, max_value=180)
    age = serializers.IntegerField(min_value=5, max_value=120)
    sex = serializers.ChoiceField(choices=Profile.Sex.choices)
    activity = serializers.ChoiceField(choices=Profile.Activity.choices)
    num_workouts = serializers.ChoiceField(choices=Profile.NumWorkouts.choices)
    goal = serializers.ChoiceField(choices=Profile.Goal.choices)

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)

    def validate_username(self, value):
        if User.objects.get(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value
    
    def create_user(self, validated_data):
        user = User.objects.create(username=validated_data["username"],
                                   password=validated_data["password"])
        return user

