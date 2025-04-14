import pickle
import numpy as np
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Load the trained model
model_filename = "Machine_Learning/heartfail.pkl"
with open(model_filename, "rb") as file:
    model = pickle.load(file)
# Manually set accuracy from training script
model_accuracy = 90  # Replace this with the actual printed accuracy value
from health.views import track_user_diseases
@login_required()
def predict_heart_failure(request):
    track_user_diseases(request, "Heart Failure")
    prediction = None
    accuracy = model_accuracy  # Pass the stored accuracy
    if request.method == "POST":
        try:
            # Manually extract values from the request
            age = float(request.POST.get("age"))
            anaemia = int(request.POST.get("anaemia"))
            creatinine_phosphokinase = int(request.POST.get("creatinine_phosphokinase"))
            diabetes = int(request.POST.get("diabetes"))
            ejection_fraction = int(request.POST.get("ejection_fraction"))
            high_blood_pressure = int(request.POST.get("high_blood_pressure"))
            platelets = float(request.POST.get("platelets"))
            serum_creatinine = float(request.POST.get("serum_creatinine"))
            serum_sodium = int(request.POST.get("serum_sodium"))
            sex = int(request.POST.get("sex"))
            smoking = int(request.POST.get("smoking"))
            time = int(request.POST.get("time"))

            # Convert input to numpy array
            data = np.array([[age, anaemia, creatinine_phosphokinase, diabetes, 
                              ejection_fraction, high_blood_pressure, platelets, 
                              serum_creatinine, serum_sodium, sex, smoking, time]]).astype(float)

            # Predict
            prediction = model.predict(data)[0]
            prediction = "You May Have Risk of Heart Failure" if prediction == 1 else "Low Risk"

        except Exception as e:
            return JsonResponse({"error": str(e)})

    return render(request, "predict.html", {"prediction": prediction, "accuracy": accuracy})



