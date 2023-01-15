from django.urls import path

from .views import PaymentHandlerAPIView

urlpatterns = [
    path("callback/", PaymentHandlerAPIView.as_view())
]
