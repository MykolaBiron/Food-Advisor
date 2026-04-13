from rest_framework import serializers
from .models import Meal, Image, Profile, WeightEntry

class ImageSerializer(serializers.Serializer):
    class Meta:
        model = Image
        fields = []


class MealSerializer(serializers.Serializer):
    class Meta:
        model = Meal
        fields = ['user', 'image', 'date', 'name', 
                  'saved', 'total_calories', 'total_proteins']
        
        
class WeightEntrySerializer(serializers.Serializer):
    class Meta:
        model = WeightEntry
        fields = ['profile', 'weight', 'date_updated']