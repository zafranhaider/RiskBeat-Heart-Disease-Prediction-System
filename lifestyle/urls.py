from django.urls import path
from .views import predict_risk

urlpatterns = [
path("", predict_risk, name="predict"),

]
