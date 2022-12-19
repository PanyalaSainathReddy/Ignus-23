from django.urls import path
from .views import CreateOrderAPIView, PaymentHandlerAPIView


urlpatterns = [
    path("pay/", CreateOrderAPIView.as_view()),
    path("callback/", PaymentHandlerAPIView.as_view())
]
