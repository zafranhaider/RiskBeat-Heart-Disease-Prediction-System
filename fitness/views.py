from django.shortcuts import render, redirect
from .models import FitnessActivity, DietaryLog, WeightEntry, UserProfile
from .forms import UserRegisterForm, ActivityForm, DietaryLogForm, WeightEntryForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

@login_required()
def activity_list(request):
    activities = FitnessActivity.objects.filter(user=request.user)
    return render(request, 'fitness/activity_list.html', {'activities': activities})
@login_required()
def custom_logout(request):
    logout(request)
    return redirect('login')
@login_required()
def diet_log(request):
    diet_logs = DietaryLog.objects.filter(user=request.user)
    return render(request, 'fitness/diet_log.html', {'diet_logs': diet_logs})


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirect to the login page after successful registration
            return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'fitness/register.html', {'form': form})

@login_required()
def home(request):
    return render(request, 'fitness/home.html')

@login_required()
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('activity_list')
    else:
        form = ActivityForm()  # Make sure this line is correct

    return render(request, 'fitness/add_activity.html', {'form': form})
@login_required()
def add_diet_log(request):
    if request.method == 'POST':
        form = DietaryLogForm(request.POST)
        if form.is_valid():
            dietary_log = form.save(commit=False)
            dietary_log.user = request.user  # Set the user to the current user
            dietary_log.save()
            return redirect('diet_log')
    else:
        form = DietaryLogForm()
    return render(request, 'fitness/add_diet_log.html', {'form': form})


@login_required()
def weight_tracker(request):
    if request.method == 'POST':
        form = WeightEntryForm(request.POST)
        if form.is_valid():
            weight_entry = form.save(commit=False)
            weight_entry.user = request.user
            weight_entry.save()
            return redirect('weight_tracker')
    else:
        form = WeightEntryForm()

    # Fetch weight entries for the graph
    weight_entries = WeightEntry.objects.filter(user=request.user).order_by('date')
    dates = [entry.date.strftime("%Y-%m-%d") for entry in weight_entries]
    weights = [entry.weight for entry in weight_entries]

    return render(request, 'fitness/weight_tracker.html', {
        'form': form, 
        'dates': dates, 
        'weights': weights
    })

from django.shortcuts import render
from health.models import Patient  # Import models from the 'health' app
@login_required()
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    patient = Patient.objects.filter(user=request.user).first()  # Fetch patient associated with logged-in user

    context = {
        'user': request.user,
        'user_profile': user_profile,
        'patient': patient  # Pass only the current user's patient
    }
    
    return render(request, 'fitness/profile.html', context)

