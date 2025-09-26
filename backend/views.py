import numpy as np
from django.shortcuts import render, redirect
from .forms import ImageForm, UserCreationForm, FoodOptionsForm, ProfileCreationForm
from .forms import CorrectPredictionForm
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .prediction_funcs import make_prediction_path
from PIL import Image as PilImage
from .nutrition_api import make_nutrition_api_call
from .models import Image, Meal, FoodItem, Profile, WeightEntry
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os 
from django.utils import timezone


def check_is_food(prediction_info):
    if prediction_info["confidence"] < 0.5:
        return False
    return True

def calculate_daily_calories(height, weight, sex, age, goal, num_workouts):
    """Calculate the amount of calories needed per day based on the users height(cm), "
    weight(kg), sport activity"""
    bias = 5
    if sex == "female":
        bias = -161
        
    calorie_intake = 10*weight + 6.25*height - 5*age + bias

    if num_workouts == "2-3":
        calorie_intake *= 1.4
    elif num_workouts == "4+": 
        calorie_intake *= 1.6
    else:
        calorie_intake *= 1.2

    if goal == "lose_weight":
        calorie_intake *= 0.9

    elif goal == "gain_weight":
        calorie_intake *= 1.1

    return calorie_intake

def calculate_daily_proteins(height, weight, sex, age, goal, num_workouts):
    calorie_intake = calculate_daily_calories(height, weight, sex, age, goal, num_workouts)
    protein_calories = calorie_intake * 0.27

    if num_workouts == "2-3":
        protein_calories *= 1.1
    elif num_workouts == "4+": 
        value *= 1.2

    return protein_calories / 4

def calculate_daily_carbs(height, weight, sex, age, goal, num_workouts):
    calorie_intake = calculate_daily_calories(height, weight, sex, age, goal, num_workouts)
    carbs_calories = calorie_intake * 0.5
    return carbs_calories / 4

def calculate_daily_fats(height, weight, sex, age,  goal, num_workouts):
    calorie_intake = calculate_daily_calories(height, weight, sex, age, goal, num_workouts)
    fats_intake = calorie_intake * 0.23
    return fats_intake / 9

def generate_weight_graph(weight_history, weight_dates, profile):
    if len(weight_history) != 0:
        fig, ax = plt.subplots(figsize=(6.5, 2.6))
        ax.set_facecolor("#333")
        ax.tick_params(axis='x', colors="#BBBBC4")
        ax.tick_params(axis='y', colors="#BBBBC4")
        ax.plot(weight_dates, weight_history, linewidth=3, color="#30A5FE")
        weight_dates = np.array(weight_dates)
        ax.set_xticks(np.linspace(weight_dates.min(), weight_dates.max(), 3))
        os.makedirs("static/images", exist_ok=True)
        plt.savefig("static/images/weight_graph.jpg", facecolor="#333")
    else:
        plt.plot(0, profile.weight)
        os.makedirs("static/images", exist_ok=True)
        plt.savefig("static/images/weight_graph.jpg", facecolor="#333")
    return 

def add_nutrition_info(context, meal):
    context["calories"] = meal.total_calories
    context["proteins"] = meal.total_proteins
    context["carbs"] = meal.total_carbs
    context["fats"] = meal.total_fats
    return context


def add_nutrition_info_api(context, option):
    context["calories"] = make_nutrition_api_call(option)["calories"]
    context["proteins"] = make_nutrition_api_call(option)["proteins"]
    context["carbs"] = make_nutrition_api_call(option)["carbs"]
    context["fats"] = make_nutrition_api_call(option)["fats"]
    return context

def landing_page(request):
    context = {}
    return render(request, "backend/landing_page.html", context)

@login_required
def start_page(request):
    # Get all user meals and sum up calories and nutrients
    saved_meals = Meal.objects.filter(user=request.user, saved=True)
    today_meals = Meal.objects.filter(user=request.user, date=timezone.now().date())
    total_calories = np.round(sum([meal.total_calories for meal in today_meals]), 2)
    total_proteins = np.round(sum([meal.total_proteins for meal in today_meals]), 2)
    total_carbs = np.round(sum([meal.total_carbs for meal in today_meals]), 2)
    total_fats = np.round(sum([meal.total_fats for meal in today_meals]), 2)

    # Get the daily nutrient targest for the user
    profile = Profile.objects.get(user=request.user)

    context = {"saved_meals": saved_meals, "choose_meal": False,
               "total_calories": total_calories, "total_proteins": total_proteins,
               "total_carbs": total_carbs, "total_fats": total_fats, "user_daily_calories": profile.calories,
               "user_daily_proteins": profile.proteins, "user_daily_carbs": profile.carbs, 
               "user_daily_fats": profile.fats}
    
    if request.method == "POST":
        context["choose_meal"] = True

    return render(request, "backend/start_page.html", context)


@login_required
def upload_photo(request, option=None):
    is_food = False

    form = ImageForm()
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            #instance.calories = calculate_calories()
            #instance.proteins = calculate_proteins()
            #instance.carbs = calculate_carbs()
            #instance.fats = calculate_fats()
            instance.save()
            prediction_info = make_prediction_path(instance.image.path)
            
            # Check if the model has enough confidence in prediction
            if check_is_food(prediction_info):
                context = prediction_info
            else:
                context = prediction_info
                context["form"] = form
                return render(request, "backend/home_page.html", context)

            
            add_nutrition_info_api(context, prediction_info["prediction"])
            meal = Meal.objects.create(
                user=request.user,
                image=instance,
                name=context["prediction"], 
                total_calories=context["calories"],
                total_proteins=context["proteins"],
                total_carbs=context["carbs"],
                total_fats=context["fats"]
            )
            meal.save()
            context["meal"] = meal
            return render(request, "backend/meal_summary.html", context)

    context = {"form": form}
    return render(request, "backend/home_page.html", context)

@login_required
def save_meal(request, meal_id):
    if request.method == "POST":
        meal = Meal.objects.get(user=request.user, id=meal_id)
        meal.saved = True
        meal.save()

    messages.success(request, "Your meal was scuccessfully saved")
    return redirect("backend:upload_photo")

def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.set_password(form.cleaned_data["password"])
            instance.username = form.cleaned_data["username"]
            instance.save()
            user = authenticate(request, password=form.cleaned_data["password"], 
                         username=form.cleaned_data["username"])
            if user is not None:
                login(request, user)
            return redirect("backend:create_profile")
        else:
            messages.error(request, "Username or password is not valid")

    context = {"form": form}
    return render(request, "backend/register.html", context)

@login_required
def create_profile(request):
    form = ProfileCreationForm()
    if request.method == "POST":
        form = ProfileCreationForm(request.POST)
        if form.is_valid():
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.height = form.cleaned_data["height"]
            profile.weight = form.cleaned_data["weight"]
            profile.age = form.cleaned_data["age"]
            profile.sex = form.cleaned_data["sex"]
            profile.activity = form.cleaned_data["activity"]
            profile.num_workouts = form.cleaned_data["num_workouts"]
            profile.goal = form.cleaned_data["goal"]

            profile.calories = calculate_daily_calories(
                form.cleaned_data["height"],
                form.cleaned_data["weight"],
                form.cleaned_data["sex"],
                form.cleaned_data["age"],
                form.cleaned_data["goal"],
                form.cleaned_data["num_workouts"])
            
            profile.proteins = calculate_daily_proteins(
                form.cleaned_data["height"],
                form.cleaned_data["weight"],
                form.cleaned_data["sex"],
                form.cleaned_data["age"],
                form.cleaned_data["goal"],
                form.cleaned_data["num_workouts"])
            
            profile.fats = calculate_daily_fats(
                form.cleaned_data["height"],
                form.cleaned_data["weight"],
                form.cleaned_data["sex"],
                form.cleaned_data["age"],
                form.cleaned_data["goal"],
                form.cleaned_data["num_workouts"])
            
            profile.save()
            return redirect("backend:start_page")
        else:
            messages.error(request, "Invalid age or sex")
        
    context = {"form": form}
    return render(request, "backend/create_profile.html", context)

@login_required
def profile(request):
    profile = None
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        return redirect("backend:create_profile")
    weight_entries = WeightEntry.objects.filter(profile=request.user.profile)
    weight_history = [weight_entry.weight for weight_entry in weight_entries]
    weight_dates = [weight_entry.date_updated for weight_entry in weight_entries]
    generate_weight_graph(weight_history, weight_dates, profile)
    context = {"profile": profile}
    return render(request, "backend/profile.html", context)

def advisor(request):
    context = {}
    return render(request, "backend/profile.html", context)


@login_required
def meal_summary(request, option):
    context = {"prediction": option}
    form = CorrectPredictionForm()
    
    # Check if meal already exists
    existing_meal = Meal.objects.filter(user=request.user, name=option).first()
    if existing_meal:
        # Use existing meal data
        add_nutrition_info(context, existing_meal)
        meal = existing_meal
    else:
        # Get nutrition info from API
        add_nutrition_info_api(context, option)
        # Create new meal without image (since no image was uploaded directly here)
        meal = Meal.objects.create(
            user=request.user,
            image=None,  # No image available when called directly
            name=option, 
            total_calories=context["calories"],
            total_proteins=context["proteins"],
            total_carbs=context["carbs"],
            total_fats=context["fats"]
        )
        meal.save()
    
    # Handle POST request for saving meal
    if request.method == "POST":
        if not meal.saved:
            meal.saved = True
            meal.save()
            messages.success(request, f"Meal '{option}' has been saved!")

    context["meal"] = meal
    context["form"] = form
    return render(request, "backend/meal_summary.html", context)


@require_POST
@login_required
def correct_prediction(request, meal_name):
    meal = Meal.objects.filter(name=meal_name, user=request.user).last()
    form = CorrectPredictionForm(request.POST)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.image = meal.image
        instance.model_prediction = meal_name
        instance.save()
        wrong_prediction = Meal.objects.filter(user=request.user, name=meal_name).last()
        wrong_prediction.delete()
        messages.success(request, "Thank you for your feedback! This helps us improve .")
        return redirect("backend:meal_summary", option=instance.correct_prediction)
    else:
        messages.error(request, "Please correct the form errors.")
        return redirect("backend:meal_summary", option=instance.correct_prediction)