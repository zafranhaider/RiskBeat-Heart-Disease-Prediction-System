from django.urls import path
from .views import home, upload_notification

urlpatterns = [
    path('', home, name='home'),
    path('upload1/', upload_notification, name='upload_notification'),
]
