from django.urls import path
from .views import EBFormAPIView, PreRegistrationFormAPIView

urlpatterns = [
    path("ebform/", EBFormAPIView.as_view()),
    path("preregform/", PreRegistrationFormAPIView.as_view())
]
