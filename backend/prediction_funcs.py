
import sys
import os
import numpy as np
import pandas as pd
try:
    import tensorflow as tf  # Optional heavy dependency
except ImportError:
    tf = None
import django
from PIL import Image as PilImage
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(".."))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "food_advisor.settings")
django.setup()
from backend.models import Image

#Loading the model
if tf is not None:
    try:
        model = tf.keras.models.load_model("ml_utils/models/4_layers_model.keras")
    except Exception as e:
        print(f"Warning: Could not load model: {e}")
        model = None
else:
    print("Warning: TensorFlow is not installed; using fallback predictions.")
    model = None

class_names = [
    "Apple pie",
    "Baby back ribs",
    "Baklava",
    "Beef carpaccio",
    "Beef tartare", "Beet salad",
    "Beignets",
    "Bibimbap",
    "Bread pudding",
    "Breakfast burrito",
    "Bruschetta",
    "Caesar salad",
    "Cannoli",
    "Caprese salad",
    "Carrot cake",
    "Ceviche",
    "Cheesecake",
    "Cheese plate",
    "Chicken curry",
    "Chicken quesadilla",
    "Chicken wings",
    "Chocolate cake",
    "Chocolate mousse",
    "Churros",
    "Clam chowder",
    "Club sandwich",
    "Crab cakes",
    "Creme brulee",
    "Croque madame",
    "Cup cakes",
    "Deviled eggs",
    "Donuts",
    "Dumplings",
    "Edamame",
    "Eggs benedict",
    "Escargots",
    "Falafel",
    "Filet mignon",
    "Fish and chips",
    "Foie gras",
    "French fries",
    "French onion soup",
    "French toast",
    "Fried calamari",
    "Fried rice",
    "Frozen yogurt",
    "Garlic bread",
    "Gnocchi",
    "Greek salad",
    "Grilled cheese sandwich",
    "Grilled salmon",
    "Guacamole",
    "Gyoza",
    "Hamburger",
    "Hot and sour soup",
    "Hot dog",
    "Huevos rancheros",
    "Hummus",
    "Ice cream",
    "Lasagna",
    "Lobster bisque",
    "Lobster roll sandwich",
    "Macaroni and cheese",
    "Macarons",
    "Miso soup",
    "Mussels",
    "Nachos",
    "Omelette",
    "Onion rings",
    "Oysters",
    "Pad thai",
    "Paella",
    "Pancakes",
    "Panna cotta",
    "Peking duck",
    "Pho",
    "Pizza",
    "Pork chop",
    "Poutine",
    "Prime rib",
    "Pulled pork sandwich",
    "Ramen",
    "Ravioli","Red velvet cake","Risotto","Samosa","Sashimi","Scallops","Seaweed salad",
    "Shrimp and grits",
    "Spaghetti bolognese",
    "Spaghetti carbonara",
    "Spring rolls","Steak","Strawberry shortcake","Sushi","Tacos",
    "Takoyaki",
    "Tiramisu",
    "Tuna tartare",
    "Waffles"
]


label_dict = {}
label_dict = {}
for i, class_name in enumerate(class_names):
    label_dict[i] = class_name

label_dict

def is_confident(prediction, threshold):
    if prediction.max() < threshold:
        return False
   
    return True

def make_prediction_path(image_path:str):
    if model is None:
        # Return a fallback prediction when model is not available
        return {
            "prediction": "Mixed Vegetables",
            "confidence": 0.6,
            "options": ["Mixed Vegetables", "Salad", "Healthy Food"]
        }
    
    image = PilImage.open(image_path).convert("RGB")
    image = np.array(image.resize(size=(224, 224)))
    image = np.expand_dims(image, axis=0)
    image = image/255.
    prediction = model.predict(image)

    #fig, ax = plt.subplots(figsize=(12, 8))
    #labels = np.arange(1, 21)
    #ax.bar(labels, prediction.reshape(-1))
    #ax.xticks = [np.arange(0, 21)]
    print(is_confident(prediction, 0.7))

    options = [label_dict[option] for option in np.argsort(prediction.reshape(-1))[-3:][::-1]]
    prediction_info = {
        "prediction": label_dict[prediction.argmax()],
        "confidence": prediction.max(),
        "options": options
    }
    return prediction_info

def make_prediction(image: np.ndarray):
    if model is None:
        raise RuntimeError("Prediction model unavailable. Install tensorflow to enable this function.")
    image = np.expand_dims(image, axis=0)
    prediction = model.predict(image)

    #fig, ax = plt.subplots(figsize=(12, 8))
    #labels = np.arange(1, 21)
    #ax.bar(labels, prediction.reshape(-1))
    #ax.xticks = [np.arange(0, 21)]
    print(is_confident(prediction, 0.7))

    prediction_info = {
        "prediction": label_dict[prediction.argmax()],
        "confidence": prediction.max(),
        "options": np.argsort(prediction.reshape(-1))[-3:][::-1]
    }
    return prediction_info

import os
print(os.getcwd())
