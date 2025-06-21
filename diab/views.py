from django.shortcuts import render
import joblib
import random
import numpy as np
from django.contrib.auth.decorators import login_required
from health.views import track_user_diseases
@login_required()
def index(request):
    track_user_diseases(request, "Diabetes")
    return render(request,"home.html")
from django.contrib.auth.decorators import login_required
import joblib
import numpy as np
from django.shortcuts import render

@login_required()
def result(request):
    cls = joblib.load('Machine_Learning/diabetes_model.sav')
    scaler = joblib.load('Machine_Learning/scaler.sav')
    lis = []

    for key in request.POST:
        if key != 'csrfmiddlewaretoken':
            lis.append(float(request.POST[key]))

    # Convert to numpy array
    input_data = np.array(lis).reshape(1, -1)
    std_data = scaler.transform(input_data)

    print("Raw input:", lis)
    print("Standardized:", input_data)

    # Custom logic: if insulin level (usually index 4) > 20
    insulin_level = lis[4]
    if insulin_level > 24:
        result = 'You have Diabetes (High Insulin Detected)'
    else:
        prediction = cls.predict(std_data)
        print("Model Prediction:", prediction[0])
        if prediction[0] == 0:
            result = 'No Diabetes'
        else:
            result = 'You have Diabetes'

    return render(request, "result.html", {'result': result})
