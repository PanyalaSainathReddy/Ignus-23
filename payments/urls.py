from django.urls import path

from .alumni import alumni_contribute, confirm_alumni_presence
from .views import (InitPaymentAPIView, PaymentCallback, bulk_payment,
                    generate_random_payment_link, random_payment,
                    update_failed_payments, update_payments,
                    verify_random_payment)

urlpatterns = [
    path("callback/", PaymentCallback.as_view()),
    path("init-payment/", InitPaymentAPIView.as_view()),
    path('update-payments/', update_payments),
    path('update-payments/failed/', update_failed_payments),
    path('generate-random-link/', generate_random_payment_link),
    path('random_payments/', random_payment),
    path('random-payment-status/', verify_random_payment),
    path('confirm-alumni-presence/', confirm_alumni_presence),
    path('alumni-contribution/', alumni_contribute),
    path('bulk-payment/', bulk_payment)
]
