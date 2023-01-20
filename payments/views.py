import json
from datetime import datetime

from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from rest_framework.views import APIView

from .models import Order, Transaction
from .utils import setupRazorpay

User = get_user_model()


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
                userprofile.amount_paid = True
                userprofile.save()
                return HttpResponseRedirect(redirect_to="https://ignus.co.in/payments/success.html")
            else:
                return HttpResponseRedirect(redirect_to="https://ignus.co.in/payments/failed.html")
        except Exception:
            return HttpResponseRedirect(redirect_to="https://ignus.co.in/payments/failed.html")
