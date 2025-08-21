import pickle
import pandas as pd
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

# Load the ML model once
model = pickle.load(open("weather_model.pkl", "rb"))
feature_names = model.feature_names_in_

# Define condition names
target_labels = [
    "Sunny", "Cloudy", "Rain", "Storm", "Fog", "Snow", "Drizzle", "Hail",
    "Thunderstorm", "Clear Night", "Partly Cloudy", "Overcast", "Freezing Rain",
    "Blizzard", "Dust Storm", "Tornado", "Haze", "Mist", "Windy", "Hot", "Cold",
    "Humid", "Dry", "Sleet", "Showers", "Heavy Rain", "Light Rain", "Ice Pellets",
    "Scattered Clouds", "Broken Clouds", "Smoke", "Ash", "Volcanic Activity",
    "Heatwave", "Extreme Cold", "Monsoon", "Light Snow", "Heavy Snow", "Flurries",
    "Tropical Storm", "Cyclone", "Hurricane", "Sandstorm", "Gale", "Breezy",
    "Calm", "Frost", "Glaze", "Thunder", "Lightning"
]

def home(request):
    if request.method == "POST":
        temp = float(request.POST.get("temp"))
        dew_point = float(request.POST.get("dew_point"))
        humidity = float(request.POST.get("humidity"))
        wind_speed = float(request.POST.get("wind_speed"))
        visibility = float(request.POST.get("visibility"))
        pressure = float(request.POST.get("pressure"))

        # Create feature dictionary
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
        prediction = model.predict(input_df)[0]

        results = [label for label, val in zip(target_labels, prediction) if val]
        print("Input Data:", input_data)
        print("Prediction Output:", prediction)
        print("Final Results:", results)


        return render(request, "home.html", {"results": results})
        
        
    return render(request, "home.html")


def about(request):
    return render(request, "about.html")

def contact(request):
    if request.method == "POST":
        # You can handle contact form submission here if needed
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")
        # For now, just render the page (you can add logic to send email/save message)
        return render(request, "contact.html", {"success": True, "name": name})
    return render(request, "contact.html")

from django.http import JsonResponse

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
        prediction = model.predict(input_df)[0]
        results = [label for label, val in zip(target_labels, prediction) if val]

        # Return the prediction as JSON
        return JsonResponse({"results": results})

    return JsonResponse({"error": "POST required"}, status=400)
    