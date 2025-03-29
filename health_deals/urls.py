from django.urls import path
from .views import home, upload_notification,notification_detail

urlpatterns = [
    path('', home, name='home3'),
    path('upload1/', upload_notification, name='upload_notification'),
    path('notification/<int:pk>/', notification_detail, name='notification_detail'),
]
