import os
import json
import pandas as pd
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from django.template.loader import get_template   # 👈 added import
from joblib import load

# ----------------------------
# Paths
# ----------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
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

# ---------- Home Page ----------
def home(request):
    context = {}

    # 👇 Debug print: tells you which home.html is being used
    print("👉 Using template:", get_template("home.html").origin)

    if request.method == "POST" and model:
        try:
            temp = float(request.POST.get("temp", 0))
            dew_point = float(request.POST.get("dew_point", 0))
            humidity = float(request.POST.get("humidity", 0))
            wind_speed = float(request.POST.get("wind_speed", 0))
            visibility = float(request.POST.get("visibility", 0))
            pressure = float(request.POST.get("pressure", 0))

            # Prepare input as DataFrame
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

            pred_index = model.predict(input_df)[0]
            result = target_labels[pred_index]
            context["result"] = result
        except Exception as e:
            context["error"] = str(e)

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
    if request.method == "POST" and model:
        try:
            temp = float(request.POST.get("temp", 0))
            dew_point = float(request.POST.get("dew_point", 0))
            humidity = float(request.POST.get("humidity", 0))
            wind_speed = float(request.POST.get("wind_speed", 0))
            visibility = float(request.POST.get("visibility", 0))
            pressure = float(request.POST.get("pressure", 0))

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

            pred_index = model.predict(input_df)[0]
            result = target_labels[pred_index]
            return JsonResponse({"result": result})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)

