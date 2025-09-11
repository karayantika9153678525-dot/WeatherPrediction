<<<<<<< HEAD
import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from joblib import load
from pathlib import Path

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent   # project root (where manage.py is)
MODEL_PATH = BASE_DIR / "weather_model.joblib"
LABELS_PATH = BASE_DIR / "target_labels.json"

# ----------------------------
# Load Model
# ----------------------------
try:
    if MODEL_PATH.exists():
        model = load(MODEL_PATH)
        feature_names = getattr(model, "feature_names_in_", [])
        print("✅ Weather Prediction Model Loaded Successfully!")
    else:
        model = None
        feature_names = []
        print(f"⚠ Model file not found at {MODEL_PATH}")
except Exception as e:
    model = None
    feature_names = []
    print(f"⚠ Error loading model: {e}")

# ----------------------------
# Load Labels
# ----------------------------
if LABELS_PATH.exists():
    with open(LABELS_PATH, "r") as f:
        target_labels = json.load(f)
else:
    target_labels = [
        "Clear", "Cloudy", "Drizzle", "Fog", "Freezing Drizzle",
        "Freezing Fog", "Freezing Rain", "Haze", "Mainly Clear",
        "Moderate Rain", "Moderate Snow", "Mostly Cloudy", "Rain",
        "Rain Showers", "Snow", "Snow Pellets", "Snow Showers", "Thunderstorms"
    ]
print("✅ Target labels loaded")


# ----------------------------
# Views
# ----------------------------
def home(request):
    prediction = None
    if request.method == "POST" and model:
        try:
            input_data = [
                float(request.POST.get("Temp_C", 0)),
                float(request.POST.get("Dew Point Temp_C", 0)),
                float(request.POST.get("Rel Hum_%", 0)),
                float(request.POST.get("Wind Speed_km/h", 0)),
                float(request.POST.get("Visibility_km", 0)),
                float(request.POST.get("Press_kPa", 0))
            ]
            pred_index = model.predict([input_data])[0]
            prediction = target_labels[pred_index]
        except Exception as e:
            prediction = f"Error: {e}"

    return render(request, "home.html", {"prediction": prediction})


def about(request):
    return render(request, "about.html")


def contact(request):
    message_sent = False
    if request.method == "POST":
        # Handle contact form logic here
        message_sent = True
    return render(request, "contact.html", {"message_sent": message_sent})


def predict_api(request):
    if request.method == "POST" and model:
        try:
            data = request.POST
            input_list = [
                float(data.get("Temp_C", 0)),
                float(data.get("Dew Point Temp_C", 0)),
                float(data.get("Rel Hum_%", 0)),
                float(data.get("Wind Speed_km/h", 0)),
                float(data.get("Visibility_km", 0)),
                float(data.get("Press_kPa", 0))
            ]
            pred_index = model.predict([input_list])[0]
            predicted_label = target_labels[pred_index]
            return JsonResponse({"prediction": predicted_label})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)



=======
import os
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from joblib import load
import json

# Paths to the ML model and labels
MODEL_PATH = os.path.join(settings.BASE_DIR, "weather_model.joblib")
LABELS_PATH = os.path.join(settings.BASE_DIR, "target_labels.json")

# Load model once at startup
model = load(MODEL_PATH)

# Features from training
feature_names = model.feature_names_in_

# Load target labels
if os.path.exists(LABELS_PATH):
    with open(LABELS_PATH, "r") as f:
        target_labels = json.load(f)
else:
    target_labels = [
        "Clear", "Cloudy", "Drizzle", "Fog", "Freezing Drizzle",
        "Freezing Fog", "Freezing Rain", "Haze", "Mainly Clear",
        "Moderate Rain", "Moderate Snow", "Mostly Cloudy", "Rain",
        "Rain Showers", "Snow", "Snow Pellets", "Snow Showers", "Thunderstorms"
    ]

# ---------- Home Page ----------
def home(request):
    context = {}
    if request.method == "POST":
        temp = float(request.POST.get("temp"))
        dew_point = float(request.POST.get("dew_point"))
        humidity = float(request.POST.get("humidity"))
        wind_speed = float(request.POST.get("wind_speed"))
        visibility = float(request.POST.get("visibility"))
        pressure = float(request.POST.get("pressure"))

        # Prepare input
        input_data = {name: 0 for name in feature_names}
        for name in feature_names:
            lname = name.lower()
            if "temp" in lname and "dew" not in lname:
                input_data[name] = temp
            elif "dew" in lname:
                input_data[name] = dew_point
            elif "humid" in lname:
                input_data[name] = humidity
            elif "wind" in lname:
                input_data[name] = wind_speed
            elif "visib" in lname:
                input_data[name] = visibility
            elif "press" in lname:
                input_data[name] = pressure

        input_df = pd.DataFrame([input_data])

        # Prediction
        pred_index = model.predict(input_df)[0]
        result = target_labels[pred_index]

        # Add result to context
        context["result"] = result

    return render(request, "home.html", context)

# ---------- About Page ----------
def about(request):
    return render(request, "about.html")

# ---------- Contact Page ----------
def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        return render(request, "contact.html", {"success": True, "name": name})
    return render(request, "contact.html")

# ---------- API Endpoint ----------
def predict_api(request):
    if request.method == "POST":
        temp = float(request.POST.get("temp"))
        dew_point = float(request.POST.get("dew_point"))
        humidity = float(request.POST.get("humidity"))
        wind_speed = float(request.POST.get("wind_speed"))
        visibility = float(request.POST.get("visibility"))
        pressure = float(request.POST.get("pressure"))

        input_data = {name: 0 for name in feature_names}
        for name in feature_names:
            lname = name.lower()
            if "temp" in lname and "dew" not in lname:
                input_data[name] = temp
            elif "dew" in lname:
                input_data[name] = dew_point
            elif "humid" in lname:
                input_data[name] = humidity
            elif "wind" in lname:
                input_data[name] = wind_speed
            elif "visib" in lname:
                input_data[name] = visibility
            elif "press" in lname:
                input_data[name] = pressure

        input_df = pd.DataFrame([input_data])

        # Prediction
        pred_index = model.predict(input_df)[0]
        result = target_labels[pred_index]

        return JsonResponse({"result": result})

    return JsonResponse({"error": "POST required"}, status=400)

>>>>>>> 556c898955d2e86d6e2bb0b002c875bce26477a0
