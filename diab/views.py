from django.shortcuts import render
import joblib
import numpy as np


def home(request):
    return render(request,"home.html")

def result(request):
    cls=joblib.load('diabetes_model.sav')
    scaler = joblib.load('scaler.sav')
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