import json
from time import time

import paytmchecksum
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from registration.models import UserProfile

from .models import Order, Transaction
from .utils import id_generator

User = get_user_model()


def get_na_orders():
    na_orders = []
    orders = Order.objects.all()

    for order in orders:
        if order.transaction_set.count() == 0:
            na_orders.append(order)

    return na_orders


def get_pending_transactions():
    return Transaction.objects.filter(status="PENDING").all()


def get_payment_status(order_id):
    mid = settings.PAYTM_MID
    merchant_key = settings.PAYTM_MERCHANT_KEY

    paytm_params = dict()
    paytm_params["body"] = {
        "mid": mid,
        "orderId": order_id
    }

    checksum = paytmchecksum.generateSignature(json.dumps(paytm_params["body"]), merchant_key)

    paytm_params["head"] = {
        "signature": checksum
    }

    data = json.dumps(paytm_params)
    url = "https://securegw.paytm.in/v3/order/status"

    response = requests.post(url, data=data, headers={"Content-type": "application/json"}).json()

    return response


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
                "custId": ignus_id,
                "mobile": userprofile.phone,
                "email": userprofile.user.email,
                "firstName": userprofile.user.first_name,
                "lastName": userprofile.user.last_name
            },
            "extendInfo": {
                "mercUnqRef": "Ignus 2023 Payments"
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


@api_view(['GET'])
def random_payment(request):
    return render(template_name='payments/random_payment.html', request=request)


@api_view(['POST'])
def generate_random_payment_link(request):
    timestamp = round(time() * 1000)
    rand = id_generator()
    ignus_id = "IG-RAN-0000"
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
            "custId": ignus_id,
        },
        "extendInfo": {
            "mercUnqRef": "Ignus 2023 Payments"
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
        user=None,
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

    link = f"https://ignus.co.in/payments/pay.html?mid={mid}&orderId={order_id}&txnToken={txnToken}"
    return HttpResponse(content=link)


@api_view(['POST'])
def update_payments(request):
    na_orders = get_na_orders()
    pending_txns = get_pending_transactions()

    updated_transactions = []

    print("Updating NA Orders...")
    for order in na_orders:
        data = get_payment_status(order.id)
        # head = data["head"]
        body = data["body"]

        txn = Transaction.objects.create(
            txn_id=body.get('txnId', ''),
            bank_txn_id=body.get('bankTxnId', ''),
            order=order,
            user=order.user,
            status=body["resultInfo"].get('resultStatus', ''),
            amount=body.get('txnAmount', ''),
            gateway_name=body.get('gatewayName', ''),
            payment_mode=body.get('paymentMode', ''),
            resp_code=body["resultInfo"].get('resultCode', ''),
            resp_msg=body["resultInfo"].get('resultMsg', ''),
            timestamp=body.get('txnDate', '')
        )
        txn.save()

        updated_transactions.append(txn)

    print("Updating Pending Transactions...")
    for t in pending_txns:
        data = get_payment_status(t.order.id)
        # head = data["head"]
        body = data["body"]

        t.txn_id = body.get('txnId', '')
        t.bank_txn_id = body.get('bankTxnId', '')
        t.status = body["resultInfo"].get('resultStatus', '')
        t.amount = body.get('txnAmount', '')
        t.gateway_name = body.get('gatewayName', '')
        t.payment_mode = body.get('paymentMode', '')
        t.resp_code = body["resultInfo"].get('resultCode', '')
        t.resp_msg = body["resultInfo"].get('resultMsg', '')
        t.timestamp = body.get('txnDate', '')

        t.save()

        updated_transactions.append(t)

    for txn in updated_transactions:
        if txn.status == 'TXN_SUCCESS':
            user = txn.user
            order = txn.order
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

    print("Updated Transactions")

    return Response(data={"message": "Transactions Updated"}, status=status.HTTP_200_OK)


class PaymentCallback(APIView):
    def post(self, request, format=None):
        print("Paytm Callback Data: ", request.data)
        from_app = False
        response_dict = {}
        secret = settings.APP_SECRET
        frontend_base_url = settings.FRONTEND_URL
        incoming_secret = request.headers.get('X-App', '')
        txn_id = request.data.get('TXNID', '')
        print("TXN ID: ", txn_id)

        if secret == incoming_secret:
            from_app = True
            response_dict = request.data

        if txn_id == '':
            if from_app:
                return Response(data={"message": "Payment Incomplete"}, status=status.HTTP_400_BAD_REQUEST)

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=incomplete")

        data = request.data
        order_id = data.get("ORDERID", '')
        checksum = data.get("CHECKSUMHASH", '')
        merchant_key = settings.PAYTM_MERCHANT_KEY
        order = Order.objects.get(id=order_id)
        user = order.user

        is_random = order_id[:11] == "IG-RAN-0000"

        txn = Transaction.objects.create(
            txn_id=txn_id,
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

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed")

        print("Checksum Matched")

        if txn.status == "TXN_FAILURE":
            # send_mail(txn)

            if from_app:
                return Response(data={"message": txn.resp_msg}, status=status.HTTP_400_BAD_REQUEST)

            if is_random:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/failed.html")

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed&msg={'-'.join(txn.resp_msg.split())}")
        elif txn.status == "PENDING":
            # send_mail(txn)

            if from_app:
                return Response(data={"message": txn.resp_msg}, status=status.HTTP_400_BAD_REQUEST)

            if is_random:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/pending.html")

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=pending&msg={'-'.join(txn.resp_msg.split())}")
        elif txn.status == "TXN_SUCCESS":
            if is_random:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/success.html")

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

            # send_mail(txn)

            if from_app:
                return Response(data={"message": "Payment Success"}, status=status.HTTP_200_OK)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/user-profile/index.html?status=success")
