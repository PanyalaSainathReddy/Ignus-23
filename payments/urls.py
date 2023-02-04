from django.urls import path

from .views import InitPaymentAPIView, PaymentCallback, update_payments

urlpatterns = [
    path("callback/", PaymentCallback.as_view()),
    path("init-payment/", InitPaymentAPIView.as_view()),
    path('update-payments/', update_payments)
]
