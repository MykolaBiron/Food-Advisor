import requests
from django.conf import settings
import environ

env = environ.Env()

BASE_URL = "https://api.nal.usda.gov/fdc/v1"
USDA_API_KEY = "B2mbaLaSSz8MwVaSaGEVQdNiCMKRavVv8BpbZQYO"

def search_food(query: str) -> dict:
    url = f"{BASE_URL}/foods/search"
    params = {
        "query": query,
        "api_key": USDA_API_KEY
    }
    response = requests.get(url, params=params)
    print(f"STATUS: {response.status_code}")
    print(f"DATA: {response.json()}")
    return response.json()

def extract_nutritions(food):
    """Extract normalized nutrient keys from USDA API response.

    Returns a dict with keys: calories, proteins, carbs, fats.
    """
    normalized = {
        "calories": 0,
        "proteins": 0,
        "carbs": 0,
        "fats": 0,
    }

    # USDA search endpoint returns nutrients under foods[0].foodNutrients.
    # Keep a fallback for older/alternate payloads that may use FoodNutrients.
    nutrients_list = []
    if isinstance(food, dict):
        foods = food.get("foods")
        if isinstance(foods, list) and foods:
            first_food = foods[0] or {}
            nutrients_list = first_food.get("foodNutrients", []) or []
        if not nutrients_list:
            nutrients_list = food.get("FoodNutrients", []) or []

    for nutrient in nutrients_list:
        name = (
            nutrient.get("nutrientName")
            or (nutrient.get("nutrient") or {}).get("name")
            or ""
        )
        value = nutrient.get("value")
        if value is None:
            value = nutrient.get("amount")

        if value is None:
            continue

        name_lower = name.lower()
        if name_lower == "energy":
            normalized["calories"] = value
        elif name_lower in {"protein", "proteins"}:
            normalized["proteins"] = value
        elif name_lower == "carbohydrate, by difference":
            normalized["carbs"] = value
        elif name_lower in {"total lipid (fat)", "total lipids (fats)"}:
            normalized["fats"] = value

    return normalized