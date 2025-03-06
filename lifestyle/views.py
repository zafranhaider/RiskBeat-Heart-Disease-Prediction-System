from django.shortcuts import render
import pandas as pd
import pickle
import numpy as np

def load_model():
    with open("Machine_Learning/life.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    return model

def heart_disease_prediction(request):
    result = None
    blood_pressure_levels = ["Low", "Normal", "Prehypertension", "Hypertension Stage 1", "Hypertension Stage 2"]
    sleep_disorder_levels = ["None", "Sleep Apnea", "Insomnia"]  # Categorical values

    if request.method == "POST":
        age = int(request.POST["age"])
        gender = request.POST["gender"]
        bmi = float(request.POST["bmi"])
        blood_pressure = request.POST["blood_pressure"]
        activity_level = int(request.POST["activity_level"])
        stress = int(request.POST["stress"])
        sleep_quality = int(request.POST["sleep_quality"])
        daily_steps = int(request.POST["daily_steps"])
        smoking = request.POST["smoking"]
        alcohol = request.POST["alcohol"]
        sleep_disorder = request.POST.get("sleep_disorder", "None")  # Prevents MultiValueDictKeyError

        # Encode categorical values
        gender = 1 if gender == "Male" else 0
        blood_pressure = blood_pressure_levels.index(blood_pressure)
        smoking = 1 if smoking == "Yes" else 0
        alcohol = 1 if alcohol == "Yes" else 0
        sleep_disorder = sleep_disorder_levels.index(sleep_disorder)  # Convert categorical sleep disorder

        # Dummy placeholder for occupation (since it was removed)
        occupation = 0  

        model = load_model()
        input_data = np.array([[age, gender, bmi, blood_pressure, activity_level, stress, sleep_quality, daily_steps, smoking, alcohol, occupation, sleep_disorder]])

        prediction = model.predict(input_data)
        result = "You have chances of heart disease." if prediction[0] == 1 else "You have low risk of heart disease."

    return render(request, "heart_form.html", {
        "result": result,
        "blood_pressure_levels": blood_pressure_levels,
        "sleep_disorder_levels": sleep_disorder_levels  # Pass to the template
    })