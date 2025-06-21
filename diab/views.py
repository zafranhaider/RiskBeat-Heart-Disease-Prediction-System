from django.shortcuts import render
import joblib
import random
import numpy as np
from django.contrib.auth.decorators import login_required
from health.views import track_user_diseases
from django.contrib.auth.decorators import login_required
import joblib
import numpy as np
from django.shortcuts import render
@login_required()
def index(request):
    track_user_diseases(request, "Diabetes")
    return render(request,"home.html")


@login_required()
def result(request):
    """
    Processes the diabetes risk assessment form submission,
    predicts risk, and renders the result page.
    Includes server-side validation for form inputs.
    """
    if request.method == 'POST':
        cls = joblib.load('Machine_Learning/diabetes_model.sav')
        scaler = joblib.load('Machine_Learning/scaler.sav')
        lis = []

        # Define the expected keys from your form in the correct order
        expected_keys = [
            'pregnancies',
            'glucose',
            'bloodpressure',
            'skinthickness',
            'insulin',
            'bmi',
            'diabetespedigreefunction',
            'age'
        ]

        # Process each input field with validation
        for key in expected_keys:
            value = request.POST.get(key) 

            if value is not None and value.strip() != '':
                try:
                    lis.append(float(value))
                except ValueError:
                    print(f"Warning: Invalid number format for {key}. Using 0.0.")
                    lis.append(0.0)
            else:
                print(f"Warning: Empty value for {key}. Using 0.0.")
                lis.append(0.0)

        if len(lis) != len(expected_keys):
            return render(request, "result.html", {'result': 'Error: Missing some input data.'})

        # Convert to numpy array
        input_data = np.array(lis).reshape(1, -1)
        std_data = scaler.transform(input_data)

        print("Raw input:", lis)
        print("Standardized:", input_data)

        # Custom logic: if insulin level (index 4 in your `lis`) > 24
        if len(lis) > 4 and lis[4] > 24:
            result_message = 'You have Diabetes (High Insulin Detected)'
        else:
            prediction = cls.predict(std_data)
            print("Model Prediction:", prediction[0])
            if prediction[0] == 0:
                result_message = 'No Diabetes'
            else:
                result_message = 'You have Diabetes'

        return render(request, "result.html", {'result': result_message})
    else:
        return render(request, "result.html", {'result': 'Invalid request method. Please submit the form.'})
