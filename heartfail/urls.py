from django.urls import path
from .views import predict_heart_failure

urlpatterns = [
    path("", predict_heart_failure, name="predict_heart_failure"),
]
