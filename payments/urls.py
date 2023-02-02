from django.urls import path

from .views import InitPaymentAPIView, PaymentCallback

urlpatterns = [
    path("callback/", PaymentCallback.as_view()),
    path("init-payment/", InitPaymentAPIView.as_view()),
]
