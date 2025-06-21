from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import pandas as pd
import numpy as np
import joblib
from health.views import track_user_diseases

# Load model and preprocessors
model = joblib.load("Machine_Learning/stroke_model.pkl")
label_encoders = joblib.load("Machine_Learning/label_encoders.pkl")
imputer = joblib.load("Machine_Learning/imputer.pkl")
scaler = joblib.load("Machine_Learning/scaler.pkl")

model_accuracy = 92  # Update with real validation score
categorical_columns = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]

@login_required()
def predict_stroke(request):
    track_user_diseases(request, "Stroke")
    prediction = None
    reason = ""
    accuracy = model_accuracy

    if request.method == "POST":
        # Extract data from form
        data = {
            "gender": request.POST.get("gender"),
            "age": float(request.POST.get("age")),
            "hypertension": int(request.POST.get("hypertension")),
            "heart_disease": int(request.POST.get("heart_disease")),
            "ever_married": request.POST.get("ever_married"),
            "work_type": request.POST.get("work_type"),
            "Residence_type": request.POST.get("Residence_type"),
            "avg_glucose_level": float(request.POST.get("avg_glucose_level")),
            "bmi": float(request.POST.get("bmi")),
            "smoking_status": request.POST.get("smoking_status"),
        }

        # --- Risk Rule Checks ---
        risk_factors = []
 
        if data["hypertension"] == 1:
            risk_factors.append("Has hypertension")
        if data["heart_disease"] == 1:
            risk_factors.append("Has heart disease")
        if data["avg_glucose_level"] > 200:
            risk_factors.append("High glucose level (>200)")
        if data["bmi"] > 30:
            risk_factors.append("Obese (BMI > 30)")
 

        # Combine reasons if any
        if risk_factors:
            reason = "Stroke May Happen : " + ", ".join(risk_factors)
        else:
            reason = "Low stroke risk based on current health indicators."

        # --- Preprocessing for ML model ---
        for col in categorical_columns:
            encoder = label_encoders[col]
            data[col] = encoder.transform([data[col]])[0]

        # Convert to DataFrame
        df_input = pd.DataFrame([data])

        # Impute missing values
        df_imputed = imputer.transform(df_input)

        # Scale features
        df_scaled = scaler.transform(df_imputed)

        # Predict using the model
        prediction = model.predict(df_scaled)[0]

    return render(request, "predict2.html", {
        "prediction": prediction,
        "accuracy": accuracy,
        "reason": reason,
    })
