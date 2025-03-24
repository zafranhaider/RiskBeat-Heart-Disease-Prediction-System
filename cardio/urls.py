from django.urls import path
from .views import predict3

urlpatterns = [
    path("", predict3, name="predict3"),
]
