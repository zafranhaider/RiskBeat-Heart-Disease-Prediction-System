import pickle
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

# Load the model once globally
MODEL_PATH = "Machine_Learning/heartdis.pkl"
with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)

# Main view for prediction
def predict4(request):
    prediction = None
    user_data = {}
    explanations = []

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

            raw_data = {
                "age": age,
                "gender": gender,
                "height": height,
                "weight": weight,
                "ap_hi": ap_hi,
                "ap_lo": ap_lo,
                "cholesterol": cholesterol,
                "gluc": gluc,
                "smoke": smoke,
                "alco": alco,
                "active": active
            }

            input_data = np.array([[age, gender, height, weight, ap_hi, ap_lo,
                                    cholesterol, gluc, smoke, alco, active]])
            pred = model.predict(input_data)
            prediction = "Risk of Heart Disease" if pred[0] == 1 else "Low Risk of Heart Disease"

            user_data = {
                "age": age,
                "gender": "Female" if gender == 1 else "Male",
                "height": height,
                "weight": weight,
                "ap_hi": ap_hi,
                "ap_lo": ap_lo,
                "cholesterol": ["Normal", "Above Normal", "High"][cholesterol - 1],
                "gluc": ["Normal", "Above Normal", "High"][gluc - 1],
                "smoke": "Yes" if smoke == 1 else "No",
                "alco": "Yes" if alco == 1 else "No",
                "active": "Yes" if active == 1 else "No",
            }

            # ➕ Get Explanation
            explanations = get_explanation(raw_data)

        except Exception as e:
            prediction = f"Error: {str(e)}"

    return render(request, "index3.html", {
        "prediction": prediction,
        "user_data": user_data,
        "explanations": explanations
    })

# PDF generation view
def generate_pdf_report(request):
    user_data = request.GET.dict()
    prediction = user_data.pop("prediction", "N/A")
    user_data["prediction"] = prediction

    template_path = 'report_template.html'
    context = {"user_data": user_data}

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="heart_report.pdf"'

    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    return response
def get_explanation(data):
    explanations = []

    # Cholesterol
    if data['cholesterol'] == 2:
        explanations.append("Your cholesterol is above normal, which increases risk.")
    elif data['cholesterol'] == 3:
        explanations.append("Your cholesterol is high — a major risk factor.")
    else:
        explanations.append("Your cholesterol level is normal — good sign.")

    # Glucose
    if data['gluc'] == 2:
        explanations.append("Your glucose is slightly high.")
    elif data['gluc'] == 3:
        explanations.append("Your glucose is very high, which increases heart risk.")
    else:
        explanations.append("Your glucose level is normal.")

    # Blood Pressure
    if data['ap_hi'] > 140 or data['ap_lo'] > 90:
        explanations.append("Your blood pressure is high, which increases cardiovascular risk.")
    elif data['ap_hi'] < 90 or data['ap_lo'] < 60:
        explanations.append("Your blood pressure is low — might be a concern.")
    else:
        explanations.append("Your blood pressure is in the normal range — good sign.")

    # Smoking
    if data['smoke'] == 1:
        explanations.append("Smoking increases risk of heart disease.")
    else:
        explanations.append("Not smoking reduces your heart disease risk.")

    # Alcohol
    if data['alco'] == 1:
        explanations.append("Alcohol consumption can contribute to heart risk.")
    else:
        explanations.append("No alcohol consumption — heart-friendly.")

    # Activity
    if data['active'] == 0:
        explanations.append("Lack of physical activity may increase your risk.")
    else:
        explanations.append("Being physically active helps your heart stay healthy.")

    return explanations
