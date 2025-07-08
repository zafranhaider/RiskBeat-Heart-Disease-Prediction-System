from django.urls import path
from .views import predict4
from .views import *
urlpatterns = [
    path("", predict4, name="predict4"),
    path("generate-pdf-report/", generate_pdf_report, name="generate_pdf_report"),
]
