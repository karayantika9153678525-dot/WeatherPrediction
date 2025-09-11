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



