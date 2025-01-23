from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, FitnessActivity, DietaryLog, WeightEntry
from django.utils import timezone

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class UserRegisterForm(forms.ModelForm):
    height = forms.IntegerField(help_text='Height in centimeters')
    weight = forms.IntegerField(help_text='Weight in kilograms')
    fitness_level = forms.IntegerField(help_text='Fitness level from 1 to 10')

    class Meta:
        model = User
        fields = ['email', 'height', 'weight', 'fitness_level']  # No password fields since user already exists

    def save(self, commit=True):
        # Retrieve the user from the database based on email
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Update UserProfile or create one if it doesn't exist
            if not user.is_superuser:  # Ensure this is not a superuser
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={
                        'height': self.cleaned_data['height'],
                        'weight': self.cleaned_data['weight'],
                        'fitness_level': self.cleaned_data['fitness_level']
                    }
                )
            return user
        else:
            raise forms.ValidationError("User with this email does not exist.")


class ActivityForm(forms.ModelForm):
    class Meta:
        model = FitnessActivity
        fields = ['activity_type', 'duration', 'intensity', 'calories_burned', 'date_time']
        widgets = {
        'date_time': forms.DateInput(format='%d/%m/%y', attrs={'type': 'date'}),
        }



class DietaryLogForm(forms.ModelForm):
    class Meta:
        model = DietaryLog
        fields = ['food_item', 'calories', 'carbs', 'proteins', 'fats', 'quantity', 'date_time']
        widgets = {
        'date_time': forms.DateInput(format='%d/%m/%y', attrs={'type': 'date'}),
        }

class WeightEntryForm(forms.ModelForm):
    class Meta:
        model = WeightEntry
        fields = ['weight', 'date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'max': timezone.now().date().isoformat()}),
        }