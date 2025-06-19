from django.urls import path
from .views import predict4

urlpatterns = [
    path("", predict4, name="predict4"),
]
