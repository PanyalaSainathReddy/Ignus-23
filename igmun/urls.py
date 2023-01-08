from django.urls import path, include
from rest_framework import routers
from .views import EBFormAPIView, PreRegistrationFormAPIView, PreCARegistrationAPIView

urlpatterns = [
    path("ebform/", EBFormAPIView.as_view()),
    path("preregform/", PreRegistrationFormAPIView.as_view()),
    path("precaregform/", PreCARegistrationAPIView.as_view()),
]
