from django.urls import path
from .views import home, upload_notification,notification_detail,subscribe_email,notify,unsubscribe_email,check_subscription

urlpatterns = [
    path('', home, name='home3'),
    path('upload1/', upload_notification, name='upload_notification'),
    path('notify/', notify, name='notify'),
    path('notification/<int:pk>/', notification_detail, name='notification_detail'),
    path('unsubscribe/', unsubscribe_email, name='unsubscribe_email'),
    path("check-subscription/", check_subscription, name="check_subscription"),
]
