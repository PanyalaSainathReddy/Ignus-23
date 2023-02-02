import json
from time import time

import paytmchecksum
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from registration.models import UserProfile

from .models import Order, Transaction
from .utils import id_generator

User = get_user_model()


class InitPaymentAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(
            user=user
        )
        ignus_id = userprofile.registration_code
        timestamp = round(time() * 1000)
        rand = id_generator()
        order_id = ignus_id+"-"+str(timestamp)+"-"+rand
        mid = settings.PAYTM_MID
        merchant_key = settings.PAYTM_MERCHANT_KEY
        amount = request.data.get('amount')
        pay_for = request.data.get('pay_for')
        paytm_params = dict()
        paytm_params["body"] = {
            "requestType": "Payment",
            "mid": mid,
            "websiteName": "WEBPROD",
            "orderId": order_id,
            "callbackUrl": "http://127.0.0.1:8000/api/payments/callback/",
            "txnAmount": {
                "value": amount,
                "currency": "INR"
            },
            "userInfo": {
                "custId": ignus_id
            }
        }

        checksum = paytmchecksum.generateSignature(json.dumps(paytm_params["body"]), merchant_key)
        paytm_params["head"] = {
            "signature": checksum
        }

        data = json.dumps(paytm_params)
        url = f"https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={mid}&orderId={order_id}"

        response = requests.post(url, data=data, headers={"Content-type": "application/json"}).json()

        txnToken = response["body"]["txnToken"]
        order = Order.objects.create(
            id=order_id,
            user=userprofile,
            checksum=checksum,
            pay_for=pay_for,
            amount=amount,
            currency="INR",
            request_timestamp=str(timestamp),
            response_timestamp=str(response["head"]["responseTimestamp"]),
            signature=response["head"]["signature"],
            result_code=response["body"]["resultInfo"]["resultCode"],
            result_msg=response["body"]["resultInfo"]["resultMsg"],
            transaction_token=txnToken
        )
        order.save()

        return Response(data={"message": "Order Created Successfully", "txnToken": txnToken, "orderId": order_id, "mid": mid}, status=status.HTTP_201_CREATED)


# class PaymentHandlerAPIView(APIView):
#     def post(self, request, format=None):
#         error = {}
#         data = request.data

#         error_code = data.get('error[code]', '')
#         if error_code:
#             error["code"] = error_code
#             error["description"] = data.get('error[description]', '')
#             error["source"] = data.get('error[source]', '')
#             error["step"] = data.get('error[step]', '')
#             error["reason"] = data.get('error[reason]', '')
#             error["metadata"] = json.loads(data.get('error[metadata]', ''))
#             payment_id = error["metadata"]["payment_id"]
#             razorpay_order_id = error["metadata"]["order_id"]
#             signature = ''
#         else:
#             payment_id = data.get('razorpay_payment_id', '')
#             razorpay_order_id = data.get('razorpay_order_id', '')
#             signature = data.get('razorpay_signature', '')

#         razorpayClient = setupRazorpay()
#         razorpayOrder = razorpayClient.order.fetch(razorpay_order_id)

#         order = Order.objects.get(id=razorpay_order_id)
#         order.amount_paid = razorpayOrder["amount_paid"]
#         order.amount_due = razorpayOrder["amount_due"]
#         order.attempts = razorpayOrder["attempts"]
#         order.save()

#         userprofile = order.user

#         payment = razorpayClient.payment.fetch(payment_id)
#         payment["created_at"] = datetime.fromtimestamp(payment["created_at"])

#         Transaction.objects.create(
#             payment_id=payment_id,
#             user=userprofile,
#             status=payment["status"],
#             order=order,
#             signature=signature,
#             captured=payment["captured"],
#             description=payment["description"],
#             email=payment["email"],
#             contact=payment["contact"],
#             fee=payment["fee"],
#             tax=payment["tax"],
#             timestamp=payment["created_at"]
#         )

#         params_dict = {
#             'razorpay_order_id': razorpay_order_id,
#             'razorpay_payment_id': payment_id,
#             'razorpay_signature': signature
#         }

#         try:
#             result = razorpayClient.utility.verify_payment_signature(params_dict)

#             if result:
#                 userprofile.amount_paid = True
#                 userprofile.save()
#                 return HttpResponseRedirect(redirect_to="https://ignus.co.in/payments/success.html")
#             else:
#                 return HttpResponseRedirect(redirect_to="https://ignus.co.in/payments/failed.html")
#         except Exception:
#             return HttpResponseRedirect(redirect_to="https://ignus.co.in/payments/failed.html")


class PaymentCallback(APIView):
    def post(self, request, format=None):
        print(request.data)
        data = request.data
        mid = data.get("MID")
        order_id = data.get("ORDERID")
        checksum = data.get("CHECKSUMHASH")
        merchant_key = settings.PAYTM_MERCHANT_KEY
        frontend_base_url = settings.FRONTEND_URL
        order = Order.objects.get(id=order_id)

        body = {
            "mid": mid,
            "orderId": order_id
        }
        body = json.dumps(body)

        verified = paytmchecksum.verifySignature(body, merchant_key, checksum)
        if not verified:
            print("Checksum Mismatched")
            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/frontend/payments/failed.html")

        txn = Transaction.objects.create(
            txn_id=data.get('TXNID')[0],
            bank_txn_id=data.get('BANKTXNID')[0],
            order=order,
            user=order.user,
            status=data.get('STATUS')[0],
            amount=data.get('TXNAMOUNT')[0],
            gateway_name=data.get('GATEWAYNAME')[0],
            payment_mode=data.get('PAYMENTMODE')[0],
            resp_code=data.get('RESPCODE')[0],
            resp_msg=data.get('RESPMSG')[0],
            timestamp=data.get('TXNDATE')[0]
        )
        txn.save()

        if txn.status == "TXN_FAILURE":
            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/frontend/payments/failed.html")
        else:
            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/frontend/payments/success.html")
