from django.shortcuts import render
from django.http import JsonResponse
import pandas as pd
import joblib
from django.urls import path

# Load saved model and encoders
model = joblib.load("Machine_Learning/stroke_model.pkl")
label_encoders = joblib.load("Machine_Learning/label_encoders.pkl")
imputer = joblib.load("Machine_Learning/imputer.pkl")



# Manually set accuracy from training script
model_accuracy = 92  # Replace this with the actual printed accuracy value

# Categorical columns used for encoding
categorical_columns = ["gender", "ever_married", "work_type", "Residence_type", "smoking_status"]

def predict_stroke(request):
    prediction = None
    accuracy = model_accuracy  # Pass the stored accuracy

    if request.method == "POST":
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
        
        # Encode categorical variables
        for col in categorical_columns:
            data[col] = label_encoders[col].transform([data[col]])[0]
        
        # Convert input data to DataFrame
        df_input = pd.DataFrame([data])
        
        # Handle missing values using imputer
        df_input["bmi"] = imputer.transform(df_input[["bmi"]])

        # Make prediction
        prediction = model.predict(df_input)[0]
        
    return render(request, "predict2.html", {"prediction": prediction, "accuracy": accuracy})
