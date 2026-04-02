from django import forms
from .models import Image, Meal
from django.contrib.auth.models import User
from .models import Profile, CorrectedPrediction

class ImageForm(forms.ModelForm):
    image = forms.ImageField(required=True)
    class Meta:
        model = Image
        fields = ['image']

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password"]

class FoodOptionsForm(forms.Form):
    option1 = forms.ChoiceField(choices=["option1", "option2", "option3"])

class MealCreationForm(forms.Form):
    class Meta:
        model = Meal
        fields = []

class ProfileCreationForm(forms.ModelForm):
    height = forms.FloatField(min_value=60, max_value=240)
    weight = forms.FloatField(min_value=30, max_value=200)

    class Meta:
        model = Profile
        fields = ["age", "sex", "weight", "height", 
                  "activity", "num_workouts", "goal"]


class WeightEntryForm(forms.Form):
    weight = forms.FloatField(
        min_value=30,
        max_value=200,
        label="Update weight (kg)",
        widget=forms.NumberInput(attrs={
            "step": "0.1",
            "placeholder": "Enter current weight",
        }),
    )

class CorrectPredictionForm(forms.ModelForm):
    correct_prediction = forms.CharField(
        label="",  # Empty label removes the text
        widget=forms.TextInput(attrs={'placeholder': 'Enter correct meal name'})
    )
    
    class Meta:
        model = CorrectedPrediction
        fields = ["correct_prediction"]
