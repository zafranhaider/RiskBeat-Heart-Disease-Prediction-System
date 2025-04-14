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
@login_required()
def result(request):
    cls=joblib.load('Machine_Learning\diabetes_model.sav')
    scaler = joblib.load('Machine_Learning\scaler.sav')
    lis=[]
    for key in request.POST:
        if key != 'csrfmiddlewaretoken':  # Exclude CSRF token from the inputs
            lis.append(float(request.POST[key]))
    
    # Convert the list to a numpy array and reshape it
    input_data = np.array(lis).reshape(1, -1)
    std_data=scaler.transform(input_data)
    print(lis, input_data)

    # Make the prediction
    
    prediction = cls.predict(std_data)
    
    print(prediction[0])
    
    result=''
    if prediction[0]==0:
        result='No Diabetes'
    else:result='You have Diabetes'
    return render(request, "result.html", {'result': result})


