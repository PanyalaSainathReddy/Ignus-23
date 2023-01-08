from django.urls import path
from .views import EBFormAPIView, PreRegistrationFormAPIView, PreCARegistrationAPIView

urlpatterns = [
    path("ebform/", EBFormAPIView.as_view()),
    path("preregform/", PreRegistrationFormAPIView.as_view()),
    path("precaregform/", PreCARegistrationAPIView.as_view()),
]
