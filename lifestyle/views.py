import joblib
import pandas as pd
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
# Load the trained model and label encoders
model = joblib.load("Machine_Learning/life.pkl")

# Define categorical mappings as used in training
label_encoders = {
    "Gender": {"Male": 0, "Female": 1},
    "Occupation": {"Engineer": 0, "Doctor": 1, "Teacher": 2, "Artist": 3, "Other": 4},
    "BMI Category": {"Underweight": 0, "Normal weight": 1, "Overweight": 2, "Obese": 3},
    "Blood Pressure": {"Normal": 0, "Elevated": 1, "High": 2},
    "Sleep Disorder": {"None": 0, "Insomnia": 1, "Sleep Apnea": 2}
}
@login_required()
def predict_risk(request):
    prediction_message = None

    if request.method == "POST":
        # Extract input data from the form
        gender = request.POST.get("gender")
        occupation = request.POST.get("occupation")
        bmi_category = request.POST.get("bmi_category")
        blood_pressure = request.POST.get("blood_pressure")
        sleep_disorder = request.POST.get("sleep_disorder")
        age = float(request.POST.get("age"))
        sleep_duration = float(request.POST.get("sleep_duration"))
        quality_of_sleep = float(request.POST.get("quality_of_sleep"))
        physical_activity = float(request.POST.get("physical_activity"))
        stress_level = float(request.POST.get("stress_level"))
        heart_rate = float(request.POST.get("heart_rate"))
        daily_steps = float(request.POST.get("daily_steps"))

        # Critical heart rate check
        if heart_rate >= 220:
            prediction_message = "💀 You are probably dead. This is not a joke. Seek emergency help immediately."
            return render(request, "predict3.html", {"prediction_message": prediction_message})
        elif heart_rate >= 180:
            prediction_message = "⚠️ Your heart rate is critically high. You are at extreme risk. Please consult a doctor immediately."
            return render(request, "predict3.html", {"prediction_message": prediction_message})

        # Encode categorical values using label encoders
        gender_encoded = label_encoders["Gender"].get(gender, -1)
        occupation_encoded = label_encoders["Occupation"].get(occupation, -1)
        bmi_encoded = label_encoders["BMI Category"].get(bmi_category, -1)
        blood_pressure_encoded = label_encoders["Blood Pressure"].get(blood_pressure, -1)
        sleep_disorder_encoded = label_encoders["Sleep Disorder"].get(sleep_disorder, -1)

        # Ensure all values are valid
        if -1 in [gender_encoded, occupation_encoded, bmi_encoded, blood_pressure_encoded, sleep_disorder_encoded]:
            return JsonResponse({"error": "Invalid input values."}, status=400)

        # Create DataFrame for model input
        input_data = pd.DataFrame([[
            gender_encoded, age, occupation_encoded, sleep_duration, quality_of_sleep,
            physical_activity, stress_level, bmi_encoded, blood_pressure_encoded,
            heart_rate, daily_steps, sleep_disorder_encoded
        ]], columns=[
            "Gender", "Age", "Occupation", "Sleep Duration", "Quality of Sleep",
            "Physical Activity Level", "Stress Level", "BMI Category",
            "Blood Pressure", "Heart Rate", "Daily Steps", "Sleep Disorder"
        ])

        # Make prediction
        prediction = model.predict(input_data)[0]

        # Convert prediction to human-readable message
        if prediction == 1:
            prediction_message = "You have chances of heart disease"
        else:
            prediction_message = "You have no risk"

    return render(request, "predict3.html", {"prediction_message": prediction_message})
