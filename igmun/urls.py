from django.urls import path
from .views import EBFormAPIView

urlpatterns = [
    path("ebform/", EBFormAPIView.as_view())
]
