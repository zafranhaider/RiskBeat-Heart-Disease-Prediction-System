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
import logging
import re
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from .models import Doctor, Booking, DoctorSlot
from datetime import datetime, timedelta, date
import json
import matplotlib.pyplot as plt
import seaborn as sns
from django.db.models import Q
sns.set_style('darkgrid')
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, HttpResponseBadRequest
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
from sklearn.model_selection import train_test_split
from .disease_data import diseases
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import datetime
from django.views.decorators.http import require_POST
from django.db import transaction

logger = logging.getLogger(__name__)
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

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('Name')
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        message = request.POST.get('Message')

        # Save the data in the database
        Contact.objects.create(name=name, email=email, subject=subject, message=message)

        # Add success message
        messages.success(request, 'Your message has been sent successfully!')
        
        return redirect('contact')  # redirect to clear form and show message

    return render(request, 'contact.html')


@login_required(login_url="login")
def view_contacts(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden("You do not have permission to access this page.")
    contacts = Contact.objects.all()  # Fetch all contacts, latest first
    return render(request, 'view_contacts.html', {'contacts': contacts})

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
        z = request.POST['experience']
        p = request.POST['pwd']
        d = request.POST['dob']
        con = request.POST['contact']
        add = request.POST['add']
        type = request.POST['type']
        im = request.FILES['image']
        dat = datetime.date.today()

        # Check if email already exists
        if User.objects.filter(email=e).exists():
            error = "email_taken"
        else:
            user = User.objects.create_user(email=e, username=u, password=p, first_name=f, last_name=l)
            if type == "Patient":
                Patient.objects.create(user=user, contact=con, address=add, image=im, dob=d)
            else:
                Doctor.objects.create(user=user, contact=con, address=add, dob=d, image=im, status=2, experience=z)
            error = "create"

    return render(request, 'register.html', {'error': error})

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


def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    selected_date = request.GET.get('date')
    
    if not doctor_id or not selected_date:
        return JsonResponse({'error': 'Missing parameters'}, status=400)
    
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
        day_name = selected_date.strftime('%A')
    except ValueError:
        return JsonResponse({'error': 'Invalid date format'}, status=400)
    
    # Get active doctor
    doctor = get_object_or_404(Doctor, id=doctor_id, status=1)
    
    # Get doctor's slots for this day of the week
    slots = DoctorSlot.objects.filter(
        doctor=doctor,
        day=day_name,
        is_active=True
    )
    
    available_slots = []
    
    for slot in slots:
        # Generate time slots within the slot's time range
        for start_time, end_time in slot.get_time_slots():
            # Check if this specific time is already booked
            is_booked = Booking.objects.filter(
                doctor=doctor,
                date=selected_date,
                time__gte=start_time,
                time__lt=end_time,
                status__in=['pending', 'approved']
            ).exists()
            
            if not is_booked:
                available_slots.append({
                    'slot_id': slot.id,
                    'start_time': start_time.strftime('%H:%M'),
                    'end_time': end_time.strftime('%H:%M'),
                    'formatted': f"{start_time.strftime('%I:%M %p')} - {end_time.strftime('%I:%M %p')}"
                })
    
    return JsonResponse({'slots': available_slots})

@login_required
def booking_form(request):
    doctors = Doctor.objects.filter(status=1)
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        contact_number = request.POST.get('contact_number')
        doctor_id = request.POST.get('doctor')
        appointment_type = request.POST.get('appointment_type')
        selected_date = request.POST.get('date')
        slot_id = request.POST.get('slot')
        start_time = request.POST.get('start_time')
        message = request.POST.get('message', '')
        
        try:
            doctor = get_object_or_404(Doctor, id=doctor_id, status=1)
            slot = get_object_or_404(DoctorSlot, id=slot_id, doctor=doctor)
            selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
            start_time = datetime.strptime(start_time, '%H:%M').time()
            
            # Check if slot is still available
            is_booked = Booking.objects.filter(
                doctor=doctor,
                date=selected_date,
                time=start_time,
                status__in=['pending', 'approved']
            ).exists()
            
            if is_booked:
                if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                    return JsonResponse({
                        'success': False,
                        'error': 'This time slot is no longer available. Please choose another time.'
                    })
                else:
                    messages.error(request, "This time slot is no longer available. Please choose another time.")
                    return render(request, 'suc.html', {
                        'doctors': doctors,
                        'form_data': request.POST
                    })
            
            # Create the booking
            Booking.objects.create(
                name=name,
                email=email,
                contact_number=contact_number,
                doctor=doctor,
                appointment_type=appointment_type,
                date=selected_date,
                slot=slot,
                time=start_time,
                message=message,
            )
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True})
            
            messages.success(request, "Appointment booked successfully!")
            return render(request, 'suc.html', {'doctors': doctors})
            
        except Exception as e:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': str(e)
                })
            else:
                messages.error(request, f"Error booking appointment: {str(e)}")
                return render(request, 'suc.html', {
                    'doctors': doctors,
                    'form_data': request.POST
                })
    
    return render(request, 'suc.html', {'doctors': doctors})



@login_required
def manage_slots(request):
    if not hasattr(request.user, 'doctor_profile'):
        messages.error(request, "Only doctors can manage slots")
        return redirect('home')

    doctor = request.user.doctor_profile

    if request.method == "POST":
        day = request.POST.get('day')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        slot_duration = request.POST.get('slot_duration', 30)

        try:
            start = datetime.strptime(start_time, '%H:%M').time()
            end = datetime.strptime(end_time, '%H:%M').time()

            if start >= end:
                messages.error(request, "End time must be after start time")
                return redirect('manage_slots')

            DoctorSlot.objects.create(
                doctor=doctor,
                day=day,
                start_time=start_time,
                end_time=end_time,
                slot_duration=slot_duration
            )
            messages.success(request, "Slot added successfully")
        except Exception as e:
            messages.error(request, f"Error adding slot: {str(e)}")

    slots = DoctorSlot.objects.filter(doctor=doctor).order_by('day', 'start_time')
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    slots_by_day = [(day, slots.filter(day=day)) for day in days_order]

    return render(request, 'manage_slots.html', {
        'slots_by_day': slots_by_day,
    })


from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone

def get_available_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date_str  = request.GET.get('date')

    if not doctor_id or not date_str:
        return JsonResponse({'slots': []})

    # parse date and get weekday
    selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
    weekday = selected_date.strftime('%A')

    # get current date/time
    today = timezone.localdate()
    now_time = timezone.localtime().time()

    slots = DoctorSlot.objects.filter(doctor_id=doctor_id, day=weekday)
    response_slots = []

    for slot in slots:
        # skip slots that started in the past if date is today
        if selected_date == today and slot.start_time <= now_time:
            continue

        is_booked = Booking.objects.filter(slot=slot, date=selected_date).exists()
        response_slots.append({
            'slot_id': slot.id,
            'start_time': str(slot.start_time),
            'formatted': f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}",
            'is_booked': is_booked
        })

    return JsonResponse({'slots': response_slots})

@login_required
@require_POST
def toggle_slot(request, slot_id):
    if not hasattr(request.user, 'doctor_profile'):
        return JsonResponse({'success': False, 'error': 'Unauthorized'})
    
    try:
        slot = DoctorSlot.objects.get(id=slot_id, doctor=request.user.doctor_profile)
        slot.is_active = not slot.is_active
        slot.save()
        return JsonResponse({
            'success': True, 
            'is_active': slot.is_active,
            'new_status': 'Active' if slot.is_active else 'Inactive'
        })
    except DoctorSlot.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Slot not found'})


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


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Doctor, Booking

@login_required
def appointment_status(request):
    try:
        # Check if the logged-in user is a doctor
        doctor = Doctor.objects.get(user=request.user)
        # Fetch bookings for the doctor
        bookings = Booking.objects.filter(doctor=doctor).order_by('-date', '-time')
    except Doctor.DoesNotExist:
        # If the user is not a doctor, fetch bookings where their email matches
        bookings = Booking.objects.filter(user=request.user).order_by('-date', '-time')

    return render(request, 'appointment_status.html', {
        'bookings': bookings
    })


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
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.92, random_state=0)

    # Initialize the model and load saved parameters if model file exists
    nn_model = XGBClassifier(
        n_estimators= 62,
        max_depth= 3,
        learning_rate= 0.09185460139255142,
        subsample= 0.9445087255877626,
        colsample_bytree= 0.9503068865846166,
        reg_alpha= 0.6822185735880166,
        reg_lambda= 4.781662063326414,
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
    track_user_diseases(request, "Cornary Disease")
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
############################ Cornary Heart Disese Logics Algoritham ########################################
########################################################################################################

def preprocess_inputs(df, scaler):
    df = df.copy()
    # Split df into X and y
    y = df['TenYearCHD'].copy()
    X = df.drop('TenYearCHD', axis=1).copy()
    X = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)
    return X, y




def prdict_cheart_disease(list_data):
    
    # Load the dataset from CSV
    csv_file_path = './Machine_Learning/cornheart.csv'  
    heart_rate = float(list_data[13])

    if heart_rate > 220:
        # Deadly heart rate
        return 0.0, [1], [("heartRate", 1.0)], "You are probably dead 💀. Call an ambulance, not a prediction site."

    elif heart_rate > 170:
        # Dangerously high
        return 0.0, [1], [("heartRate", 1.0)], "⚠️ Dangerously high heart rate! You are at serious risk of heart disease."

    # Read the CSV file
    df = pd.read_csv(csv_file_path)

    X = df[['male', 'age', 'education', 'currentSmoker', 'cigsPerDay', 'BPMeds',
            'prevalentStroke', 'prevalentHyp', 'diabetes', 'totChol', 'sysBP', 'diaBP',
            'BMI', 'heartRate', 'glucose']]
    y = df['TenYearCHD']
    X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.82, random_state=0)

    # Initialize the model and load saved parameters if model file exists
    nn_model = XGBClassifier(
    n_estimators= 251,
    max_depth= 3,
    learning_rate= 0.035998012016241976,
    subsample= 0.9775449686982007,
    colsample_bytree= 0.8149219334036141,
    reg_alpha= 0.9601641553647629,
    reg_lambda= 2.1747392006396034,
    )

    # Load the pre-trained model if it exists
    try:
        nn_model.load_model('./Machine_Learning/cornheart.json')  # Add the path to the saved model
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
    return (nn_model.score(X_test, y_test) * 100), pred, important_factors, None




@login_required(login_url="login")
def add_conrheartdetail(request):
    track_user_diseases(request, "Cornary Disease")
    
    if request.method == "POST":
        required_fields = [
            "male", "age", "education", "currentSmoker", "cigsPerDay",
            "BPMeds", "prevalentStroke", "prevalentHyp", "diabetes",
            "totChol", "sysBP", "diaBP", "BMI", "heartRate", "glucose"
        ]
        
        list_data = []
        errors = []
        
        # Validate each field
        for field in required_fields:
            value = request.POST.get(field)
            if value is None or value.strip() == '':
                errors.append(f"Field '{field}' is required.")
            else:
                try:
                    list_data.append(float(value))
                except ValueError:
                    errors.append(f"Invalid value for '{field}'. Must be a number.")
        
        if errors:
            return render(request, 'cornheart.html', {'error': ", ".join(errors)})
        
        try:
            # Perform prediction with message handling
            accuracy, pred, feature_contributions, custom_message = prdict_cheart_disease(list_data)
            
            # Save prediction results
            patient = Patient.objects.get(user=request.user)
            Search_Data.objects.create(
                patient=patient,
                prediction_accuracy=accuracy,
                result=pred[0],
                values_list=list_data,
            )
            
            # Fetch doctors based on patient's address
            patient_address = patient.address
            doctors = Doctor.objects.filter(address__icontains=patient_address)

            # Final prediction message
            pred_message = custom_message if custom_message else (
                "Low risk of 10-year coronary heart disease." if pred[0] == 0 else "High risk of 10-year coronary heart disease."
            )
            
            return render(request, 'corn_pred.html', {
                'accuracy': accuracy,
                'pred': pred[0],
                'pred_message': pred_message,
                'contributing_factors': feature_contributions,
                'doctors': doctors
            })
        
        except Patient.DoesNotExist:
            return render(request, 'cornheart.html', {'error': "Patient profile not found."})
        except Exception as e:
            logger.error(f"Error in add_conrheartdetail: {e}", exc_info=True)
            return render(request, 'cornheart.html', {'error': str(e)})

    return render(request, 'cornheart.html')

@login_required(login_url="login")
def predict_corndesease(request):
    try:
        # Get patient address
        patient = Patient.objects.get(user=request.user)
        patient_address = patient.address
        
        # Fetch doctors based on patient's address
        doctors = Doctor.objects.filter(address__icontains=patient_address)

        # Perform prediction (assuming you have a function for this)
        accuracy, pred = predict_corn_disease()  # Update with the actual function

        # Prepare prediction message
        pred_message = "Low Risk" if pred == 0 else "High Risk"

        # Save prediction results
        Search_Data.objects.create(
            patient=patient,
            prediction_accuracy=accuracy,
            result=pred,
        )

        # Render template with context
        return render(request, 'corn_pred.html', {
            'accuracy': accuracy,
            'pred': pred,
            'pred_message': pred_message,
            'doctors': doctors
        })

    except Patient.DoesNotExist:
        return render(request, 'corn_pred.html', {'error': "Patient profile not found."})
    except Exception as e:
        logger.error(f"Error in predict_corndesease: {e}", exc_info=True)
        return render(request, 'corn_pred.html', {'error': str(e)})

########################################################################################################
############################ Life Assessment Logics Algoritham ########################################
########################################################################################################



















########################################################################################################
############################ Extra Features ########################################
########################################################################################################



@login_required()
def check_disease(request):
    matched_diseases = []

    if request.method == 'POST':
        user_input = request.POST.get('symptoms', '').lower().replace(" ", "")  # Remove spaces for better matching
        
        for disease in diseases:
            disease_symptoms = disease['symptoms'].lower().replace(" ", "")  # Remove spaces for better matching
            
            # Check for partial matches (e.g., "chestpa" should match "chest pain")
            if re.search(user_input, disease_symptoms):  
                matched_diseases.append(disease)

    return render(request, 'Diss_view.html', {'diseases': matched_diseases})


import random

import random
from django.contrib import messages

ALL_DISEASES = [
    "Diabetes", "Cardiovascular Disease", "Stroke", "Heart Failure",
    "Cornary Disease"
]

def track_user_diseases(request, current_disease):
    if 'viewed_diseases' not in request.session:
        request.session['viewed_diseases'] = []

    if 'suggestion_shown' not in request.session:
        request.session['suggestion_shown'] = False

    viewed = request.session['viewed_diseases']
    if current_disease not in viewed:
        viewed.append(current_disease)
        request.session['viewed_diseases'] = viewed
        request.session['suggestion_shown'] = False  # Reset on new disease view

    if not request.session['suggestion_shown']:
        unvisited = list(set(ALL_DISEASES) - set(viewed))
        if unvisited:
            suggestion = random.choice(unvisited)
            messages.info(request, f"According to This Submission You May also Try checking out: {suggestion}")
            request.session['suggestion_shown'] = True





def check_slots(request):
    """
    GET params: doctor_id, date (YYYY-MM-DD)
    Returns every sub-slot (start→end) that:
      • Comes from an active DoctorSlot
      • Falls on that weekday
      • Isn’t already booked at that exact start time
    """
    doctor_id = request.GET.get('doctor_id')
    date_str  = request.GET.get('date')
    date      = datetime.strptime(date_str, '%Y-%m-%d').date()
    weekday   = date.strftime('%A')  # “Monday”,…

    # all matching definitions
    defs = DoctorSlot.objects.filter(
      doctor_id=doctor_id,
      day=weekday,
      is_active=True
    )
    available = []
    for ds in defs:
        for start, end in ds.get_time_slots():
            # skip if already booked:
            if Booking.objects.filter(slot=ds, date=date, time=start).exists():
                continue
            available.append({
                'slot_def_id': ds.id,
                'start': start.strftime('%H:%M'),
                'end':   end.strftime('%H:%M'),
            })

    return JsonResponse({'slots': available})


from django.shortcuts import get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.db import transaction
from datetime import datetime

from .models import DoctorSlot, Booking

@require_POST
@transaction.atomic
def book_appointment(request):
    # 1) Ensure AJAX:
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return HttpResponseBadRequest("Invalid request type")

    try:
        # 2) Parse the chosen slot
        raw = request.POST['chosen_slot']   # e.g. "17|09:30"
        slot_id, start_time = raw.split('|')
        date = datetime.strptime(request.POST['date'], '%Y-%m-%d').date()

        # 3) Lookup and lock the slot
        slot = get_object_or_404(DoctorSlot, pk=slot_id, is_active=True)

        # 4) Attempt create (unique_together prevents dupes)
        booking, created = Booking.objects.get_or_create(
            slot=slot,
            date=date,
            time=start_time,
                user=request.user,              # ← add this

            defaults={
                        'user': request.user,                # ← add this

                'name': request.POST['name'],
                'email': request.POST['email'],
                'contact_number': request.POST['contact_number'],
                'doctor': slot.doctor,
                'appointment_type': request.POST['appointment_type'],
                'message': request.POST.get('message', ''),
            }
        )

        if not created:
            return JsonResponse({
                'success': False,
                'error': 'Sorry, that slot was just taken.'
            })

        return JsonResponse({'success': True})

    except KeyError:
        return JsonResponse({'success': False, 'error': 'Missing form data.'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
