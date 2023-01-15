import razorpay
from django.conf import settings


def setupRazorpay():
    razorpayClient = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    razorpayClient.set_app_details({"title": "IGNUS '23", "version": "1.0.0"})

    return razorpayClient
