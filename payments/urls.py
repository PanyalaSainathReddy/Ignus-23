from django.urls import path

from .alumni import alumni_contribute, confirm_alumni_presence
from .views import (InitPaymentAPIView, PaymentCallback, bulk_payment,
                    generate_random_payment_link, payment_500,
                    payment_500_statuses, random_payment, update_payments,
                    verify_random_payment)

urlpatterns = [
    path("callback/", PaymentCallback.as_view()),
    path("init-payment/", InitPaymentAPIView.as_view()),
    path('payment-500/', payment_500),
    path('payment-500/statuses/', payment_500_statuses),
    path('update-payments/', update_payments),
    path('generate-random-link/', generate_random_payment_link),
    path('random_payments/', random_payment),
    path('random-payment-status/', verify_random_payment),
    path('confirm-alumni-presence/', confirm_alumni_presence),
    path('alumni-contribution/', alumni_contribute),
    path('bulk-payment/', bulk_payment)
]
