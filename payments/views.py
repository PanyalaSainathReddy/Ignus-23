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
        callback_url = "https://api.ignus.co.in/api/payments/callback/"
        mid = settings.PAYTM_MID
        merchant_key = settings.PAYTM_MERCHANT_KEY
        amount = request.data.get('amount')
        pay_for = request.data.get('pay_for', '')
        paytm_params = dict()
        paytm_params["body"] = {
            "requestType": "Payment",
            "mid": mid,
            "websiteName": "WEBPROD",
            "orderId": order_id,
            "callbackUrl": callback_url,
            "txnAmount": {
                "value": amount,
                "currency": "INR"
            },
            "userInfo": {
                "custId": ignus_id
            },
            "extendInfo": {
                "mercUnqRef": f"Ignus {ignus_id}"
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


class PaymentCallback(APIView):
    def post(self, request, format=None):
        from_app = False
        response_dict = {}
        secret = settings.APP_SECRET
        incoming_secret = request.headers.get('X-App', '')

        if secret == incoming_secret:
            from_app = True
            response_dict = request.data

        data = request.data
        order_id = data.get("ORDERID", '')
        checksum = data.get("CHECKSUMHASH", '')
        merchant_key = settings.PAYTM_MERCHANT_KEY
        frontend_base_url = settings.FRONTEND_URL
        order = Order.objects.get(id=order_id)
        user = order.user

        txn = Transaction.objects.create(
            txn_id=data.get('TXNID', ''),
            bank_txn_id=data.get('BANKTXNID', ''),
            order=order,
            user=user,
            status=data.get('STATUS', ''),
            amount=data.get('TXNAMOUNT', ''),
            gateway_name=data.get('GATEWAYNAME', ''),
            payment_mode=data.get('PAYMENTMODE', ''),
            resp_code=data.get('RESPCODE', ''),
            resp_msg=data.get('RESPMSG', ''),
            timestamp=data.get('TXNDATE', '')
        )
        txn.save()

        if not from_app:
            form = request.POST

            for i in form.keys():
                response_dict[i] = form[i]
                if i == 'CHECKSUMHASH':
                    checksum = form[i]

        verified = paytmchecksum.verifySignature(response_dict, merchant_key, checksum)

        if not verified:
            print("Checksum Mismatched")

            if from_app:
                return Response(data={"message": "Invalid Payment"}, status=status.HTTP_400_BAD_REQUEST)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed")

        print("Checksum Matched")

        if txn.status == "TXN_FAILURE":
            if from_app:
                return Response(data={"message": "Payment Failed"}, status=status.HTTP_400_BAD_REQUEST)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed")
        elif txn.status == "PENDING":
            if from_app:
                return Response(data={"message": "Payment Pending"}, status=status.HTTP_400_BAD_REQUEST)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=pending")
        elif txn.status == "TXN_SUCCESS":
            pay_for = order.pay_for

            if pay_for == "pass-499.00":
                user.amount_paid = True
                user.pronites = True
                user.main_pronite = True
                user.igmun = False
            elif pay_for == "pass-2299.00":
                user.amount_paid = True
                user.pronites = True
                user.main_pronite = True
                user.accomodation_4 = True
                user.igmun = False
            elif pay_for == "pass-1500.00":
                user.amount_paid = True
                user.pronites = True
                user.main_pronite = True
                user.igmun = True
            elif pay_for == "pass-2500.00":
                user.amount_paid = True
                user.pronites = True
                user.main_pronite = True
                user.igmun = True
                user.accomodation_2 = True
            elif pay_for == "pass-1499.00":
                if user.amount_paid is True:
                    user.flagship = True

            user.save()

            if from_app:
                return Response(data={"message": "Payment Success"}, status=status.HTTP_200_OK)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/user-profile/index.html?status=success")
