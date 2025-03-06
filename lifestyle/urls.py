from django.urls import path
from .views import heart_disease_prediction

urlpatterns = [
    path('', heart_disease_prediction, name='heart_disease_prediction'),
]
