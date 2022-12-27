from datetime import datetime
# from .serializers import OrderSerializer
from .models import Order, Transaction
# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
from rest_framework.views import APIView
import json
# from django.middleware import csrf
from django.contrib.auth import get_user_model
# from registration.models import UserProfile
from django.http.response import HttpResponseRedirect
from .utils import setupRazorpay

User = get_user_model()


# class CreateOrderAPIView(generics.CreateAPIView):
#     permission_classes = (IsAuthenticated,)
#     serializer_class = OrderSerializer

#     def create(self, request, *args, **kwargs):
#         user = User.objects.get(id=request.user.id)
#         userprofile = UserProfile.objects.get(user=user)
#         numOrders = Order.objects.count()
#         data = {
#             "amount": userprofile.amount_due * 100,
#             "currency": "INR",
#             "receipt": f"order_rcptid_{numOrders+1}"
#         }
#         paymentOrder = razorpayClient.order.create(data=data)
#         paymentOrder["created_at"] = datetime.fromtimestamp(paymentOrder["created_at"])

#         order = Order.objects.create(
#             id=paymentOrder["id"],
#             user=userprofile,
#             amount=paymentOrder["amount"] // 100,
#             amount_paid=paymentOrder["amount_paid"] // 100,
#             amount_due=paymentOrder["amount_due"] // 100,
#             currency=paymentOrder["currency"],
#             receipt=paymentOrder["receipt"],
#             attempts=paymentOrder["attempts"],
#             timestamp=paymentOrder["created_at"]
#         )

#         order = OrderSerializer(order)

#         response = Response(status=status.HTTP_201_CREATED)
#         response.set_cookie(
#             key='order_id',
#             value=order.data["id"],
#             expires=datetime.strftime(datetime.utcnow() + timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
#             secure=False,
#             httponly=False,
#             samesite='Lax'
#         )
#         response.set_cookie(
#             key='amount_due',
#             value=order.data["amount_due"] * 100,
#             expires=datetime.strftime(datetime.utcnow() + timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
#             secure=False,
#             httponly=False,
#             samesite='Lax'
#         )
#         response.set_cookie(
#             key='currency',
#             value=order.data["currency"],
#             expires=datetime.strftime(datetime.utcnow() + timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
#             secure=False,
#             httponly=False,
#             samesite='Lax'
#         )
#         response["X-CSRFToken"] = csrf.get_token(request)

#         return response


class PaymentHandlerAPIView(APIView):
    def post(self, request, format=None):
        error = {}
        data = request.data

        error_code = data.get('error[code]', '')
        if error_code:
            error["code"] = error_code
            error["description"] = data.get('error[description]', '')
            error["source"] = data.get('error[source]', '')
            error["step"] = data.get('error[step]', '')
            error["reason"] = data.get('error[reason]', '')
            error["metadata"] = json.loads(data.get('error[metadata]', ''))
            payment_id = error["metadata"]["payment_id"]
            razorpay_order_id = error["metadata"]["order_id"]
            signature = ''
        else:
            payment_id = data.get('razorpay_payment_id', '')
            razorpay_order_id = data.get('razorpay_order_id', '')
            signature = data.get('razorpay_signature', '')

        razorpayClient = setupRazorpay()
        razorpayOrder = razorpayClient.order.fetch(razorpay_order_id)

        order = Order.objects.get(id=razorpay_order_id)
        order.amount_paid = razorpayOrder["amount_paid"]
        order.amount_due = razorpayOrder["amount_due"]
        order.attempts = razorpayOrder["attempts"]
        order.save()

        userprofile = order.user

        payment = razorpayClient.payment.fetch(payment_id)
        payment["created_at"] = datetime.fromtimestamp(payment["created_at"])

        Transaction.objects.create(
            payment_id=payment_id,
            user=userprofile,
            status=payment["status"],
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
                userprofile.amount_paid = True
                userprofile.save()
                return HttpResponseRedirect(redirect_to="http://127.0.0.1:5500/frontend/payments/success.html")
            else:
                print("Payment Failed!")
                return HttpResponseRedirect(redirect_to="http://127.0.0.1:5500/frontend/payments/failed.html")
        except Exception:
            print("Payment Failed!")
            return HttpResponseRedirect(redirect_to="http://127.0.0.1:5500/frontend/payments/failed.html")
