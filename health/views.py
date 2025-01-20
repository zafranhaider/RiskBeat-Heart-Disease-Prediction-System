from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import datetime
from xgboost import XGBClassifier  # Import XGBClassifier
from .forms import DoctorForm
from .models import *
from django.contrib.auth import authenticate, login, logout
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from django.db.models import Q
sns.set_style('darkgrid')
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split

from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from django.http import HttpResponse


########################################################################################################
############################ Pages Templates ########################################
########################################################################################################
def Home(request):
    dis = Feedback.objects.all()  # Fetch feedback data from the Feedback model
    return render(request, 'carousel.html', {'dis': dis})


def Admin_Home(request):
    dis = Search_Data.objects.all()
    pat = Patient.objects.all()
    doc = Doctor.objects.all()
    feed = Feedback.objects.all()

    d = {'dis':dis.count(),'pat':pat.count(),'doc':doc.count(),'feed':feed.count()}
    return render(request,'admin_home.html',d)



@login_required(login_url="login")
def User_Home(request):
    return render(request,'patient_home.html')

@login_required(login_url="login")
def User_book(request):
    doctors = Doctor.objects.all()
    return render(request, 'apoint_page.html', {'doctors': doctors})


@login_required(login_url="login")
def Doctor_Home(request):
    return render(request,'doctor_home.html')

def About(request):
    return render(request,'about.html')

def Contact(request):
    return render(request,'contact.html')


def Gallery(request):
    return render(request,'gallery.html')


@login_required(login_url="login")
def delete_doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    doc.delete()
    return redirect('view_doctor')

@login_required(login_url="login")
def delete_feedback(request,pid):
    doc = Feedback.objects.get(id=pid)
    doc.delete()
    return redirect('view_feedback')

@login_required(login_url="login")
def delete_patient(request,pid):
    doc = Patient.objects.get(id=pid)
    doc.delete()
    return redirect('view_patient')

@login_required(login_url="login")
def delete_searched(request,pid):
    doc = Search_Data.objects.get(id=pid)
    doc.delete()
    return redirect('view_search_pat')

@login_required(login_url="login")
def View_Doctor(request):
    doc = Doctor.objects.all()
    d = {'doc':doc}
    return render(request,'view_doctor.html',d)

@login_required(login_url="login")
def View_Patient(request):
    patient = Patient.objects.all()
    d = {'patient':patient}
    return render(request,'view_patient.html',d)

@login_required(login_url="login")
def View_Feedback(request):
    dis = Feedback.objects.all()
    d = {'dis':dis}
    return render(request,'view_feedback.html',d)
########################################################################################################
############################ Authtentications Logics  ########################################
########################################################################################################

def Login_User(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        sign = ""
        if user:
            try:
                sign = Patient.objects.get(user=user)
            except:
                pass
            if sign:
                login(request, user)
                error = "pat1"
            else:
                pure=False
                try:
                    pure = Doctor.objects.get(status=1,user=user)
                except:
                    pass
                if pure:
                    login(request, user)
                    error = "pat2"
                else:
                    login(request, user)
                    error="notmember"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'login.html', d)

def Login_admin(request):
    error = ""
    if request.method == "POST":
        u = request.POST['uname']
        p = request.POST['pwd']
        user = authenticate(username=u, password=p)
        if user.is_staff:
            login(request, user)
            error="pat"
        else:
            error="not"
    d = {'error': error}
    return render(request, 'admin_login.html', d)

def Signup_User(request):
    error = ""
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        u = request.POST['uname']
        e = request.POST['email']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()
        user = User.objects.create_user(email=e, username=u, password=p, first_name=f,last_name=l)
        if type == "Patient":
            Patient.objects.create(user=user,contact=con,address=add,image=im,dob=d)
        else:
            Doctor.objects.create(dob=d,image=im,user=user,contact=con,address=add,status=2)
        error = "create"
    d = {'error':error}
    return render(request,'register.html',d)

def Logout(request):
    logout(request)
    return redirect('home')

@login_required(login_url="login")
def Change_Password(request):
    sign = 0
    user = User.objects.get(username=request.user.username)
    error = ""
    if not request.user.is_staff:
        try:
            sign = Patient.objects.get(user=user)
            if sign:
                error = "pat"
        except:
            sign = Doctor.objects.get(user=user)
    terror = ""
    if request.method=="POST":
        n = request.POST['pwd1']
        c = request.POST['pwd2']
        o = request.POST['pwd3']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            terror = "yes"
        else:
            terror = "not"
    d = {'error':error,'terror':terror,'data':sign}
    return render(request,'change_password.html',d)


########################################################################################################
############################ Main Logics Starts here  ########################################
########################################################################################################

@login_required(login_url="login")
def assign_status(request,pid):
    doctor = Doctor.objects.get(id=pid)
    if doctor.status == 1:
        doctor.status = 2
        messages.success(request, 'Selected doctor are successfully withdraw his approval.')
    else:
        doctor.status = 1
        messages.success(request, 'Selected doctor are successfully approved.')
    doctor.save()
    return redirect('view_doctor')

@login_required(login_url="login")
def add_doctor(request,pid=None):
    doctor = None
    if pid:
        doctor = Doctor.objects.get(id=pid)
    if request.method == "POST":
        form = DoctorForm(request.POST, request.FILES, instance = doctor)
        if form.is_valid():
            new_doc = form.save()
            new_doc.status = 1
            if not pid:
                user = User.objects.create_user(password=request.POST['password'], username=request.POST['username'], first_name=request.POST['first_name'], last_name=request.POST['last_name'])
                new_doc.user = user
            new_doc.save()
            return redirect('view_doctor')
    d = {"doctor": doctor}
    return render(request, 'add_doctor.html', d)




@login_required(login_url="login")
def view_search_pat(request):
    data = None
    try:
        # Check if the user is a doctor
        doc = Doctor.objects.get(user=request.user)
        # Fetch all Search_Data if the user is a doctor
        data = Search_Data.objects.all().order_by('-id')
    except Doctor.DoesNotExist:
        try:
            # If not a doctor, check if the user is a patient
            patient = Patient.objects.get(user=request.user)
            data = Search_Data.objects.filter(patient=patient).order_by('-id')
        except Patient.DoesNotExist:
            # If neither a doctor nor a patient, fallback to admin logic
            data = Search_Data.objects.all().order_by('-id')
    return render(request, 'view_search_pat.html', {'data': data})




@login_required(login_url="login")
def View_My_Detail(request):
    terror = ""
    user = User.objects.get(id=request.user.id)
    error = ""
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    d = {'error': error,'pro':sign}
    return render(request,'profile_doctor.html',d)

@login_required(login_url="login")
def Edit_Doctor(request,pid):
    doc = Doctor.objects.get(id=pid)
    error = ""
    # type = Type.objects.all()
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        cat = request.POST['type']
        try:
            im = request.FILES['image']
            doc.image=im
            doc.save()
        except:
            pass
        dat = datetime.date.today()
        doc.user.first_name = f
        doc.user.last_name = l
        doc.user.email = e
        doc.contact = con
        doc.category = cat
        doc.address = add
        doc.user.save()
        doc.save()
        error = "create"
    d = {'error':error,'doc':doc,'type':type}
    return render(request,'edit_doctor.html',d)

@login_required(login_url="login")
def Edit_My_deatail(request):
    terror = ""
    print("Hii welvome")
    user = User.objects.get(id=request.user.id)
    error = ""
    # type = Type.objects.all()
    try:
        sign = Patient.objects.get(user=user)
        error = "pat"
    except:
        sign = Doctor.objects.get(user=user)
    if request.method == 'POST':
        f = request.POST['fname']
        l = request.POST['lname']
        e = request.POST['email']
        con = request.POST['contact']
        add = request.POST['add']
        try:
            im = request.FILES['image']
            sign.image = im
            sign.save()
        except:
            pass
        to1 = datetime.date.today()
        sign.user.first_name = f
        sign.user.last_name = l
        sign.user.email = e
        sign.contact = con
        if error != "pat":
            cat = request.POST['type']
            sign.category = cat
            sign.save()
        sign.address = add
        sign.user.save()
        sign.save()
        terror = "create"
    d = {'error':error,'terror':terror,'doc':sign}
    return render(request,'edit_profile.html',d)

@login_required(login_url='login')
def sent_feedback(request):
    terror = None
    if request.method == "POST":
        username = request.POST['uname']
        message = request.POST['msg']
        rating = request.POST['rating']  # Get the rating from the form
        username = User.objects.get(username=username)
        Feedback.objects.create(user=username, messages=message, rating=rating)
        terror = "create"
    return render(request, 'sent_feedback.html', {'terror': terror})


@login_required
def search_doctor(request):
    t = None  # To determine which type of search was performed
    doc = []  # To hold the filtered results
    li = []  # Placeholder for additional filtering if necessary

    if request.method == "POST":
        search_type = request.POST.get("type")
        search_text = request.POST.get("tex")

        if search_type == "Name":
            # Filter using Q objects for first_name and last_name from the related User model
            doc = Doctor.objects.filter(
                Q(user__first_name__icontains=search_text) | Q(user__last_name__icontains=search_text)
            )
            t = "Name"

        elif search_type == "Type":
            doc = Doctor.objects.filter(category__icontains=search_text)
            t = "Type"

        elif search_type == "Address":
            doc = Doctor.objects.filter(address__icontains=search_text)
            t = "Address"

    return render(request, 'search_doctor.html', {
        't': t,
        'doc': doc,
        'li': li  # Include any additional filtering logic here
    })
from .disease_data import diseases
@login_required
def view_diseases(request):
    return render(request, 'Diss_view.html', {'diseases': diseases})



@login_required
def booking_form(request):
    doctors = Doctor.objects.filter(status=1)  # Show only active doctors
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        contact_number = request.POST['contact_number']
        doctor_id = request.POST['doctor']
        appointment_type = request.POST['appointment_type']
        date = request.POST['date']
        time = request.POST['time']
        message = request.POST.get('message', '')

        doctor = get_object_or_404(Doctor, id=doctor_id)
        booking = Booking.objects.create(
            name=name,
            email=email,
            contact_number=contact_number,
            doctor=doctor,
            appointment_type=appointment_type,
            date=date,
            time=time,
            message=message,
        )
      

    return render(request, 'suc.html', {'doctors': doctors})

@login_required
def update_booking_status(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    if request.method == "POST":
        status = request.POST.get("status")
        if status in ['approved', 'rejected', 'unavailable']:  # Include 'unavailable' status
            booking.status = status
            booking.save()
            # Redirect to the appointments page after updating the status
            return redirect('view_appointments')
    return HttpResponse("Invalid request", status=400)


@login_required
def view_appointments(request):
    doctor = get_object_or_404(Doctor, user=request.user)
    # Filter out appointments that are not pending
    appointments = Booking.objects.filter(doctor=doctor, status='pending')
    return render(request, 'apoint_view.html', {'appointments': appointments})


@login_required
def appointment_status(request):
    try:
        # Check if the logged-in user is a doctor
        doctor = Doctor.objects.get(user=request.user)
        # Fetch bookings for the doctor
        user_bookings = Booking.objects.filter(doctor=doctor)
    except Doctor.DoesNotExist:
        # If the user is not a doctor, fetch bookings where their email matches
        user_bookings = Booking.objects.filter(email=request.user.email)

    return render(request, 'appointment_status.html', {'bookings': user_bookings})


########################################################################################################
############################ Machine Learning Logics Algoritham ########################################
########################################################################################################


########################################################################################################
############################ Heart Disese Logics Algoritham ########################################
########################################################################################################

def preprocess_inputs(df, scaler):
    df = df.copy()
    # Split df into X and y
    y = df['target'].copy()
    X = df.drop('target', axis=1).copy()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    return X, y


FEATURE_NAME_MAP = {
    'age': 'Age',
    'sex': 'Sex',
    'cp': 'Chest Pain Type',
    'trestbps': 'Resting Blood Pressure',
    'chol': 'Cholesterol',
    'fbs': 'Fasting Blood Sugar',
    'restecg': 'Resting ECG Results',
    'thalach': 'Maximum Heart Rate Achieved',
    'exang': 'Exercise Induced Angina',
    'oldpeak': 'ST Depression Induced by Exercise',
    'slope': 'Slope of the Peak Exercise ST Segment',
    'ca': 'Number of Major Vessels Colored by Fluoroscopy',
    'thal': 'Thalassemia'
}


def prdict_heart_disease(list_data):
    # Load the dataset from CSV
    csv_file_path = './Machine_Learning/heart.csv'  

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    X = df[['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']]
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.82, random_state=0)

    # Initialize the model and load saved parameters if model file exists
    nn_model = XGBClassifier(
        n_estimators=166,
        max_depth= 6,
        learning_rate= 0.024732561568874125,
        subsample= 0.7805684973814158,
        colsample_bytree= 0.9389311570118616,
        reg_alpha= 0.7406459603133639,
        reg_lambda= 2.904335752371348,
        random_state=0,
    )

    # Load the pre-trained model if it exists
    try:
        nn_model.load_model('./Machine_Learning/heart.json')  # Add the path to the saved model
        print("Model loaded successfully!")
    except Exception as e:
        print("No pre-trained model found, training a new model...")
        nn_model.fit(X_train, y_train)  # Train a new model if the saved one doesn't exist

    # Convert input to proper format
    list_data = np.array([list_data], dtype=np.float32)
    pred = nn_model.predict(list_data)
    
    # Feature importance extraction
    feature_importances = nn_model.feature_importances_
    feature_names = X.columns
    important_factors = [
        (FEATURE_NAME_MAP.get(feature_names[i], feature_names[i]), feature_importances[i]) 
        for i in range(len(feature_importances))
    ]
    important_factors.sort(key=lambda x: x[1], reverse=True)

    return (nn_model.score(X_test, y_test) * 100), pred, important_factors



@login_required(login_url="login")
def add_heartdetail(request):
    if request.method == "POST":
        list_data = []
        value_dict = eval(str(request.POST)[12:-1])
        count = 0
        for key, value in value_dict.items():
            if count == 0:
                count = 1
                continue
            if key == "sex" and value[0].lower() in ['male', 'm']:
                list_data.append(1)
                continue
            elif key == "sex":
                list_data.append(0)
                continue
            list_data.append(value[0])

        accuracy, pred, feature_contributions = prdict_heart_disease(list_data)
        patient = Patient.objects.get(user=request.user)
        Search_Data.objects.create(patient=patient, prediction_accuracy=accuracy, result=pred[0], values_list=list_data)
        
        if pred[0] == 0:
            pred_message = "You are healthy."
        else:
            pred_message = "You may possess a risk of heart disease."
        
        return render(request, 'predict_disease.html', {
            'accuracy': accuracy,
            'pred': pred[0],
            'pred_message': pred_message,
            'contributing_factors': feature_contributions
        })
    return render(request, 'add_heartdetail.html')

@login_required(login_url="login")
def predict_desease(request, pred, accuracy):
    # Fetching the logged-in user's address
    patient_address = Patient.objects.get(user=request.user).address

    # Filtering doctors based on the patient's address
    doctor = Doctor.objects.filter(address__icontains=patient_address)

    # Preparing context data for the template
    context = {
        'pred': pred,
        'accuracy': accuracy,
        'doctor': doctor,
        'pred_message': 'High Risk' if pred else 'Low Risk'
    }

    # Rendering the template with the context data
    return render(request, 'predict_disease.html', context)


########################################################################################################
############################ Life Assessment Logics Algoritham ########################################
########################################################################################################