from django.urls import path
from .views import PaymentHandlerAPIView


urlpatterns = [
    # path("pay/", CreateOrderAPIView.as_view()),
    path("callback/", PaymentHandlerAPIView.as_view())
]
