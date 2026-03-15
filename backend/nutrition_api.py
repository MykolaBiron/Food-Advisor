import requests

APP_ID = "2f6f4895"
API_KEY = "cd40eb0aa38abe6e36931da97d409901"

def make_nutrition_api_call(query:str) -> dict:
    """Make a call to nutritionix api using a query (food name)
        Return a dict containing he info about the food"""
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "query": query
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes
        response_dict = response.json()
        
        # Check if 'foods' key exists and has at least one item
        if "foods" not in response_dict or len(response_dict["foods"]) == 0:
            print(f"Warning: No foods found in API response for query: {query}")
            print(f"API Response: {response_dict}")
            # Return default values
            return {
                "calories": 200,
                "proteins": 10,
                "carbs": 25,
                "fats": 8
            }
        
        # Extract nutrition info from the first food item
        result = {}
        food_item = response_dict["foods"][0]
        result["calories"] = food_item.get("nf_calories", 200)
        result["proteins"] = food_item.get("nf_protein", 10)
        result["carbs"] = food_item.get("nf_total_carbohydrate", 25)
        result["fats"] = food_item.get("nf_total_fat", 8)
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Error making nutrition API call for '{query}': {e}")
        # Return default values when API fails
        return {
            "calories": 200,
            "proteins": 10,
            "carbs": 25,
            "fats": 8
        }
    except (KeyError, IndexError) as e:
        print(f"Error parsing nutrition API response for '{query}': {e}")
        print(f"Response: {response_dict if 'response_dict' in locals() else 'No response'}")
        # Return default values when parsing fails
        return {
            "calories": 200,
            "proteins": 10,
            "carbs": 25,
            "fats": 8
        }
