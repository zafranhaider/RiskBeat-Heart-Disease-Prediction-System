import pickle
import numpy as np
from django.shortcuts import render
from health.views import track_user_diseases
# Load the trained model
MODEL_PATH = "Machine_Learning/cardio.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

def predict3(request):
    track_user_diseases(request, "Cardiovascular Disease")
    prediction = None  # Default

    if request.method == "POST":
        try:
            # Collect input values
            age = int(request.POST["age"])
            gender = int(request.POST["gender"])
            height = int(request.POST["height"])
            weight = float(request.POST["weight"])
            ap_hi = int(request.POST["ap_hi"])
            ap_lo = int(request.POST["ap_lo"])
            cholesterol = int(request.POST["cholesterol"])
            gluc = int(request.POST["gluc"])
            smoke = int(request.POST["smoke"])
            alco = int(request.POST["alco"])
            active = int(request.POST["active"])

            # Prepare data for prediction
            input_data = np.array([[age, gender, height, weight, ap_hi, ap_lo, 
                                    cholesterol, gluc, smoke, alco, active]])
            
            # Make prediction using the loaded model
            pred = model.predict(input_data)
            prediction = "Risk of Cardiovascular Disease" if pred[0] == 1 else "Low Risk"
        
        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render(request, "index1.html", {"prediction": prediction})
