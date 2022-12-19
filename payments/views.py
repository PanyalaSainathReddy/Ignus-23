import razorpay
from django.conf import settings
from datetime import datetime
from .serializers import OrderSerializer
from .models import Order, Transaction
from rest_framework import generics, status
# from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import json

razorpayClient = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
razorpayClient.set_app_details({"title": "IGNUS '23", "version": "1.0.0"})


class CreateOrderAPIView(generics.CreateAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # user = User.objects.get(id=request.user.id)
        # userprofile = UserProfile.objects.get(user=user)
        numOrders = Order.objects.count()
        data = {"amount": 500, "currency": "INR", "receipt": f"order_rcptid_{numOrders+1}"}
        paymentOrder = razorpayClient.order.create(data=data)
        paymentOrder["created_at"] = datetime.fromtimestamp(paymentOrder["created_at"])

        order = Order.objects.create(
            id=paymentOrder["id"],
            # user=userprofile,
            amount=paymentOrder["amount"],
            amount_paid=paymentOrder["amount_paid"],
            amount_due=paymentOrder["amount_due"],
            currency=paymentOrder["currency"],
            receipt=paymentOrder["receipt"],
            attempts=paymentOrder["attempts"],
            timestamp=paymentOrder["created_at"]
        )

        order = OrderSerializer(order)

        return Response(data=order.data, status=status.HTTP_201_CREATED)


class PaymentHandlerAPIView(APIView):
    def post(self, request, format=None):
        error = {}
        data = request.data

        error = data.get('error', '')
        if error:
            payment_id = error["metadata"]["payment_id"]
            razorpay_order_id = error["metadata"]["order_id"]
            signature = ''
        else:
            payment_id = data.get('razorpay_payment_id', '')
            razorpay_order_id = data.get('razorpay_order_id', '')
            signature = data.get('razorpay_signature', '')

        razorpayOrder = razorpayClient.order.fetch(razorpay_order_id)

        order = Order.objects.get(id=razorpay_order_id)
        order.amount_paid = razorpayOrder["amount_paid"]
        order.amount_due = razorpayOrder["amount_due"]
        order.attempts = razorpayOrder["attempts"]
        order.save()

        payment = razorpayClient.payment.fetch(payment_id)
        payment["created_at"] = datetime.fromtimestamp(payment["created_at"])

        Transaction.objects.create(
            payment_id=payment_id,
            order=order,
            signature=signature,
            captured=payment["captured"],
            description=payment["description"],
            email=payment["email"],
            contact=payment["contact"],
            fee=payment["fee"],
            tax=payment["tax"],
            timestamp=payment["created_at"]
        )

        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        try:
            result = razorpayClient.utility.verify_payment_signature(params_dict)

            if result:
                print("Payment Successful!")
                return Response(data={"status": "Payment Successful"}, status=status.HTTP_200_OK)

            else:
                print("Payment Failed!")
                return Response(data={"status": "Payment Failed", "error": json.dumps(error)}, status=status.HTTP_200_OK)
        except Exception:
            print("Payment Failed!")
            return Response(data={"status": "Payment Failed", "error": json.dumps(error)}, status=status.HTTP_200_OK)
