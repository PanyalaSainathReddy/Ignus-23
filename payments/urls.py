from django.urls import path

from .views import (InitPaymentAPIView, PaymentCallback, alumni_contribute,
                    bulk_payment, confirm_alumni_presence,
                    generate_random_payment_link, random_payment,
                    update_payments, verify_random_payment)

urlpatterns = [
    path("callback/", PaymentCallback.as_view()),
    path("init-payment/", InitPaymentAPIView.as_view()),
    path('update-payments/', update_payments),
    path('generate-random-link/', generate_random_payment_link),
    path('random_payments/', random_payment),
    path('random-payment-status/', verify_random_payment),
    path('confirm-alumni-presence/', confirm_alumni_presence),
    path('alumni-contribution/', alumni_contribute),
    path('bulk-payment/', bulk_payment)
]
