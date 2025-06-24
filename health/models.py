from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import User
from datetime import time
# Create your models here.
from .choices import DOCTOR_STATUS

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    dob = models.DateField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username



class Doctor(models.Model):
    DOCTOR_STATUS = [(1, "Active"), (0, "Inactive")]
    status = models.IntegerField(choices=DOCTOR_STATUS, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True)
    contact = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=100, null=True)
    experience = models.CharField(max_length=100, null=True)
    category = models.CharField(max_length=100, null=True)
    doj = models.DateField(null=True)
    dob = models.DateField(null=True)
    image = models.FileField(null=True)

    def __str__(self):
        return self.user.username

class DoctorSlot(models.Model):
    DAY_CHOICES = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
    ]
    
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    slot_duration = models.PositiveIntegerField(help_text="Duration in minutes", default=30)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        unique_together = ('doctor', 'day', 'start_time', 'end_time')
    
    def __str__(self):
        return f"{self.doctor.user.username} - {self.day} {self.start_time}-{self.end_time}"

    def get_time_slots(self):
        """Generate all possible time slots within this time range"""
        slots = []
        current_time = self.start_time
        while True:
            end_time = self._add_minutes(current_time, self.slot_duration)
            if end_time > self.end_time:
                break
            slots.append((current_time, end_time))
            current_time = end_time
        return slots

    def _add_minutes(self, time_obj, minutes):
        """Add minutes to a time object"""
        total_minutes = time_obj.hour * 60 + time_obj.minute + minutes
        return time(hour=total_minutes // 60, minute=total_minutes % 60)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('unavailable', 'Unavailable'),
    ]
    
    APPOINTMENT_TYPES = [
        ('in_person', 'In-Person'),
        ('virtual', 'Virtual'),
    ]
    
    user           = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name           = models.CharField(max_length=100)
    email          = models.EmailField()
    contact_number = models.CharField(max_length=15)
    doctor         = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True)
    appointment_type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES)
    date           = models.DateField()
    slot           = models.ForeignKey(DoctorSlot, on_delete=models.CASCADE, null=True)
    time           = models.TimeField()
    message        = models.TextField(null=True, blank=True)
    status         = models.CharField(max_length=11, choices=STATUS_CHOICES, default='pending')

    class Meta:
        unique_together = ('slot','date','time')

    def __str__(self):
        return f"{self.user.username if self.user else self.name} – {self.date} {self.time}"


class DoctorRating(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ratings')
    doctor  = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='ratings')
    score   = models.PositiveSmallIntegerField(choices=[(i,i) for i in range(1,6)])
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('patient','doctor')

    def __str__(self):
        return f"{self.patient.user.username} → {self.doctor.user.username}: {self.score}★"


class Admin_Helath_CSV(models.Model):
    name = models.CharField(max_length=100, null=True)
    csv_file = models.FileField(null=True, blank=True)

    def __str__(self):
        return self.name

class Search_Data(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True)
    prediction_accuracy = models.CharField(max_length=100,null=True,blank=True)
    result = models.CharField(max_length=100,null=True,blank=True)
    values_list = models.CharField(max_length=100,null=True,blank=True)
    created = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.patient.user.username

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    messages = models.TextField(null=True)
    date = models.DateField(auto_now=True)
    rating = models.PositiveSmallIntegerField(null=True, choices=[(i, i) for i in range(1, 6)])  # Ratings from 1 to 5

    def __str__(self):
        return self.user.username

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    # models.py
from django.db import models
from django.contrib.auth.models import User
from datetime import time

# … your existing Patient, Doctor, DoctorSlot, Booking, etc. …

class DayAvailability(models.Model):
    DAY_CHOICES = [
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
    ]
    doctor      = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="day_availabilities")
    day         = models.CharField(max_length=9, choices=DAY_CHOICES)
    is_available= models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor','day')

    def __str__(self):
        return f"{self.doctor.user.username} – {self.day} {'✓' if self.is_available else '✗'}"
