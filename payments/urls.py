from django.urls import path

from .views import InitPaymentAPIView, PaymentCallback, update_payments, generate_random_payment_link, random_payment

urlpatterns = [
    path("callback/", PaymentCallback.as_view()),
    path("init-payment/", InitPaymentAPIView.as_view()),
    path('update-payments/', update_payments),
    path('generate-random-link/', generate_random_payment_link),
    path('random_payments/', random_payment)
]
