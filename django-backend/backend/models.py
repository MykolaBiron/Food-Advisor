from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Image(models.Model):
    """Store images that users upload"""
    image = models.ImageField(upload_to="images/")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user}"
    
class FoodItem(models.Model):
    calories_per_100g = models.FloatField(default=0)
    proteins_per_100g = models.FloatField(default=0)
    carbs_per_100g = models.FloatField(default=0)
    fats_per_100g = models.FloatField(default=0)

class Meal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=200)
    saved = models.BooleanField(default=False)
    total_calories = models.FloatField(default=0)
    total_proteins = models.FloatField(default=0)
    total_fats = models.FloatField(default=0)
    total_carbs = models.FloatField(default=0)

    def __str__(self):
        return self.name[:50]


class MealItem(models.Model):
    class Size(models.TextChoices):
        SMALL = "small", "Small"
        MIDDLE = "middle", "Middle"
        LARGE = "large", "Large"

    serving_size = models.CharField(choices=Size.choices, default=Size.MIDDLE)
    food_item = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)


class Profile(models.Model):
    class Sex(models.TextChoices):
        MAN = "male", "male"
        WOMEN = "female", "female"
        DIVERSE = "diverse", "diverse"

    class Goal(models.TextChoices):
        LOOSE_WEIGHT = "lose_weight", "Lose weight"
        MAINTAIN_WEIGHT = "maintain_weight", "Maintain weight"
        GAIN_WEIGHT = "gain_weight", "Gain weight"

    class Activity(models.TextChoices):
        LOW = "low", "Low"
        MODERATE = "moderate", "Moderate"
        HIGH = "high", "High"
    class NumWorkouts(models.TextChoices):
        ZERO_ONE = "0-1", "0-1 workouts per week"
        TWO_THREE = "2-3", "2-3 workouts per week"
        FOUR_OR_MORE = "4+", "4+ workouts per week"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(default=20)
    sex = models.CharField(choices=Sex.choices)
    height = models.IntegerField(default=180, validators=[MinValueValidator(60), MaxValueValidator(240)])
    weight = models.FloatField(default=75, validators=[MinValueValidator(30), MaxValueValidator(200)])
    goal = models.CharField(choices=Goal.choices, default=Goal.MAINTAIN_WEIGHT)
    activity = models.CharField(choices=Activity.choices, default=Activity.MODERATE)
    num_workouts = models.CharField(choices=NumWorkouts.choices, default=NumWorkouts.ZERO_ONE)
    calories = models.IntegerField(default=2000, validators=[MinValueValidator(600)])
    proteins = models.IntegerField(default=95, validators=[MinValueValidator(30)])
    carbs = models.IntegerField(default=150, validators=[MinValueValidator(40)])
    fats = models.IntegerField(default=150, validators=[MinValueValidator(20)])

    def __str__(self):
        return f"{self.user.username}"


class WeightEntry(models.Model):
    """Store the current weight of the user everytime it changes"""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    weight = models.FloatField(default=75, validators=[MinValueValidator(30), MaxValueValidator(200)])
    date_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.profile.user.username} {self.weight:.2f} kg"
    
class CorrectedPrediction(models.Model):
    """Store the wrong prediction of the model and the correct label entered by user"""
    image = models.ImageField(upload_to="images/corrected_predictions")
    model_prediction = models.CharField(max_length=200)
    correct_prediction = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.model_prediction} -> {self.correct_prediction}"

