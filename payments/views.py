import json
import logging
from time import time
from urllib.parse import quote_plus
import paytmchecksum
import requests
from django.conf import settings
from django.contrib.auth import get_user_model
from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from events.models import Event, TeamRegistration
from registration.models import UserProfile
from .models import BulkOrder, BulkTransaction, Order, PromoCode, Transaction
from .utils import (get_na_orders, get_payment_status,
                    get_pending_transactions, id_generator)

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
        promo_code = request.data.get('promo_code', '')
        promo = None

        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code)

                if pay_for[:10] == promo.pass_name[:10]:
                    if promo.is_valid():
                        amount = promo.discounted_amount
                    else:
                        return Response(data={"message": "Promo Code Expired!"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"message": "Promo Code is not valid for this Pass"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(data={"message": "Invalid Promo Code"}, status=status.HTTP_400_BAD_REQUEST)

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
            promo_code=promo,
            currency="INR",
            request_timestamp=str(timestamp),
            response_timestamp=str(response["head"]["responseTimestamp"]),
            signature=response["head"]["signature"],
            result_code=response["body"]["resultInfo"]["resultCode"],
            result_msg=response["body"]["resultInfo"]["resultMsg"],
            transaction_token=txnToken
        )
        order.save()

        return Response(
            data={
                "message": "Order Created Successfully",
                "txnToken": txnToken,
                "orderId": order_id,
                "mid": mid
            },
            status=status.HTTP_201_CREATED
        )


class UpgradeToIGMUNAPIView(APIView):
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
        promo_code = request.data.get('promo_code', '')
        promo = None

        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code)

                if pay_for[:10] == promo.pass_name[:10]:
                    if promo.is_valid():
                        amount = promo.discounted_amount
                    else:
                        return Response(data={"message": "Promo Code Expired!"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"message": "Promo Code is not valid for this Pass"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(data={"message": "Invalid Promo Code"}, status=status.HTTP_400_BAD_REQUEST)

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
            promo_code=promo,
            currency="INR",
            request_timestamp=str(timestamp),
            response_timestamp=str(response["head"]["responseTimestamp"]),
            signature=response["head"]["signature"],
            result_code=response["body"]["resultInfo"]["resultCode"],
            result_msg=response["body"]["resultInfo"]["resultMsg"],
            transaction_token=txnToken
        )
        order.save()

        userprofile.igmun_pref = request.data.get('igmun_pref', '')
        userprofile.mun_exp = request.data.get('mun_exp', '')
        userprofile.save()

        return Response(
            data={
                "message": "Order Created Successfully",
                "txnToken": txnToken,
                "orderId": order_id,
                "mid": mid
            },
            status=status.HTTP_201_CREATED
        )


class UpgradeToGoldAPIView(APIView):
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
        pay_for = "gold-upgrade"
        promo_code = request.data.get('promo_code', '')
        promo = None

        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code)

                if pay_for[:10] == promo.pass_name[:10]:
                    if promo.is_valid():
                        amount = promo.discounted_amount
                    else:
                        return Response(data={"message": "Promo Code Expired!"}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response(data={"message": "Promo Code is not valid for this Pass"}, status=status.HTTP_400_BAD_REQUEST)
            except Exception:
                return Response(data={"message": "Invalid Promo Code"}, status=status.HTTP_400_BAD_REQUEST)

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
            promo_code=promo,
            currency="INR",
            request_timestamp=str(timestamp),
            response_timestamp=str(response["head"]["responseTimestamp"]),
            signature=response["head"]["signature"],
            result_code=response["body"]["resultInfo"]["resultCode"],
            result_msg=response["body"]["resultInfo"]["resultMsg"],
            transaction_token=txnToken
        )
        order.save()

        return Response(
            data={
                "message": "Order Created Successfully",
                "txnToken": txnToken,
                "orderId": order_id,
                "mid": mid
            },
            status=status.HTTP_201_CREATED
        )


@api_view(['POST'])
def bulk_payment(request):
    timestamp = round(time() * 1000)
    rand = id_generator()
    ignus_id = "IG-BUL-0000"
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
            "mobile": request.data.get('phone', ''),
            "email": request.data.get('email', ''),
            "firstName": request.data.get('first_name'),
            "lastName": request.data.get('last_name')
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
    order = BulkOrder.objects.create(
        id=order_id,
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

    for user_id in request.data.get('users'):
        if UserProfile.objects.filter(registration_code=user_id).exists():
            order.users.add(UserProfile.objects.get(registration_code=user_id))
    order.save()

    link = f"https://ignus.co.in/payments/pay.html?mid={mid}&orderId={order_id}&txnToken={txnToken}"
    return HttpResponseRedirect(redirect_to=link)


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
    qr_base_url = "https://chart.apis.google.com/chart?chs=500x500&cht=qr&choe=UTF-8"
    qr = mark_safe(f'{qr_base_url}&chl={quote_plus(link)}')

    return render(
        request=request,
        template_name='payments/random_payment.html',
        context={
            "link": link,
            'qr_code': qr
        }
    )


@api_view(['POST'])
def payment_500(request):
    timestamp = round(time() * 1000)
    rand = id_generator()
    ignus_id = "IG-500-0000"
    order_id = ignus_id+"-"+str(timestamp)+"-"+rand
    callback_url = "https://api.ignus.co.in/api/payments/callback/"
    mid = settings.PAYTM_MID
    merchant_key = settings.PAYTM_MERCHANT_KEY
    name = request.data.get('name')
    amount = request.data.get('amount')
    pay_for = name + "; " + request.data.get('remarks', '')
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
            "firstName": name
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

    return Response(data={"link": link}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def payment_500_statuses(request):
    orders = [order.id for order in Order.objects.all() if order.id[:11] == "IG-500-0000"]
    orders = Order.objects.filter(id__in=orders)

    data = []

    for order in orders:
        name, remarks = order.pay_for.split("; ")
        order_id = order.id
        order_status = get_payment_status(order_id=order_id)["body"]["resultInfo"].get('resultStatus', '')

        d = {
            "name": name,
            "remarks": remarks,
            "status": order_status,
            "order_id": order_id
        }
        data.append(d)

    return Response(data={"data": data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def verify_random_payment(request):
    data = request.data
    link = data.get('link', '')

    if link == '':
        return render(request=request, template_name='payments/random_payment.html')

    order_id = link.split('?')[1].split('&')[1].split('=')[1]
    data = get_payment_status(order_id=order_id)
    status = data["body"]["resultInfo"].get('resultStatus', '')

    qr_base_url = "https://chart.apis.google.com/chart?chs=500x500&cht=qr&choe=UTF-8"
    qr = mark_safe(f'{qr_base_url}&chl={quote_plus(link)}')

    return render(
        request=request,
        template_name='payments/random_payment.html',
        context={
            "link": link,
            "status": status,
            "qr_code": qr
        }
    )


@api_view(['POST'])
def update_payments(request):
    na_orders = get_na_orders()
    pending_txns = get_pending_transactions()

    updated_transactions = []

    logging.info(msg="Updating NA Orders...")
    for order in na_orders:
        data = get_payment_status(order.id)
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

    logging.info(msg="Updating Pending Transactions...")
    for t in pending_txns:
        data = get_payment_status(t.order.id)
        body = data["body"]

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
        order_id = txn.order.id
        if order_id[:11] == "IG-RAN-0000" or order_id[:11] == "IG-ALU-0000":
            pass
        else:
            if txn.status == 'TXN_SUCCESS':
                user = txn.user
                order = txn.order
                pay_for = order.pay_for
                if order.promo_code:
                    order.promo_code.use()

                if pay_for == "pass-499.00":
                    user.amount_paid = True
                    user.pronites = True
                    user.main_pronite = True
                    user.igmun = False
                elif pay_for == "pass-799.00":
                    user.amount_paid = True
                    user.pronites = True
                    user.main_pronite = True
                    user.igmun = False
                    user.is_gold = True
                elif pay_for == "gold-upgrade":
                    user.is_gold = True
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
                elif pay_for == "pass-1800.00":
                    user.accomodation_4 = True
                elif pay_for == "pass-1000.00":
                    user.accomodation_2 = True
                elif pay_for == "pass-1499.00-antarang":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.antarang = True
                        event = Event.objects.get(name='Antarang')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()
                elif pay_for == "pass-1499.00-nrityansh":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.nrityansh = True
                        event = Event.objects.get(name='Nrityansh')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()
                elif pay_for == "pass-1499.00-aayaam":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.aayaam = True
                        event = Event.objects.get(name='Aayaam')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()
                elif pay_for == "pass-1499.00-clashofbands":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.cob = True
                        event = Event.objects.get(name='Thunder Beats')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()
                elif pay_for == "pass-200.00-dance-workshop":
                    event = Event.objects.get(name='Dance Workshop')
                    user.events_registered.add(event)
                elif pay_for == "pass-129.00-resinart-workshop":
                    event = Event.objects.get(name='Resin Art Workshop')
                    user.events_registered.add(event)
                elif pay_for == "pass-100.00-music-workshop":
                    event = Event.objects.get(name='Music Workshop')
                    user.events_registered.add(event)
                elif pay_for == "pass-100.00-filmmaking-workshop":
                    event = Event.objects.get(name='Film Making Workshop')
                    user.events_registered.add(event)
                elif pay_for == "pass-150.00-pottery-workshop":
                    event = Event.objects.get(name='Pottery Workshop')
                    user.events_registered.add(event)
                elif pay_for == "pass-150.00-phadpainting-workshop":
                    event = Event.objects.get(name='Phad Painting Workshop')
                    user.events_registered.add(event)
                elif pay_for == "pass-150.00-papercutting-workshop":
                    event = Event.objects.get(name='Paper Cutting Workshop')
                    user.events_registered.add(event)

                user.save()

    logging.info(msg="Updated Transactions")

    return Response(data={"message": "Transactions Updated"}, status=status.HTTP_200_OK)


class PaymentCallback(APIView):
    def post(self, request, format=None):
        logging.info(msg=f"Paytm Callback Data: {request.data}")
        from_app = False
        response_dict = {}
        secret = settings.APP_SECRET
        frontend_base_url = settings.FRONTEND_URL
        incoming_secret = request.headers.get('X-App', '')
        txn_id = request.data.get('TXNID', '')
        logging.info(msg=f"TXN ID: {txn_id}")

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

        is_random = order_id[:11] == "IG-RAN-0000"
        is_alumni = order_id[:11] == "IG-ALU-0000"
        bulk_order = order_id[:11] == "IG-BUL-0000"
        is_500 = order_id[:11] == "IG-500-0000"

        if bulk_order:
            order = BulkOrder.objects.get(id=order_id)
            users = order.users

            txn = BulkTransaction.objects.create(
                txn_id=txn_id,
                bank_txn_id=data.get('BANKTXNID', ''),
                order=order,
                users=users,
                status=data.get('STATUS', ''),
                amount=data.get('TXNAMOUNT', ''),
                gateway_name=data.get('GATEWAYNAME', ''),
                payment_mode=data.get('PAYMENTMODE', ''),
                resp_code=data.get('RESPCODE', ''),
                resp_msg=data.get('RESPMSG', ''),
                timestamp=data.get('TXNDATE', '')
            )
            txn.save()
        else:
            order = Order.objects.get(id=order_id)
            user = order.user

            if Transaction.objects.filter(txn_id=txn_id).exists():
                txn = Transaction.objects.get(txn_id=txn_id)

                txn.bank_txn_id = data.get('BANKTXNID', '')
                txn.status = data.get('STATUS', '')
                txn.amount = data.get('TXNAMOUNT', '')
                txn.gateway_name = data.get('GATEWAYNAME', '')
                txn.payment_mode = data.get('PAYMENTMODE', '')
                txn.resp_code = data.get('RESPCODE', '')
                txn.resp_msg = data.get('RESPMSG', '')
                txn.timestamp = data.get('TXNDATE', '')
            else:
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
            logging.debug(msg="Checksum Mismatched")

            if from_app:
                return Response(data={"message": "Invalid Payment"}, status=status.HTTP_400_BAD_REQUEST)

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed")

        logging.debug(msg="Checksum Matched")

        if txn.status == "TXN_FAILURE":
            if from_app:
                return Response(data={"message": txn.resp_msg}, status=status.HTTP_400_BAD_REQUEST)

            if is_random or bulk_order:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/failed.html")

            if is_alumni:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/alumni/index.html?status=failed")

            if is_500:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/failed.html")

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed&msg={'-'.join(txn.resp_msg.split())}")
        elif txn.status == "PENDING":
            if from_app:
                return Response(data={"message": txn.resp_msg}, status=status.HTTP_400_BAD_REQUEST)

            if is_random or bulk_order:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/pending.html")

            if is_alumni:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/alumni/index.html?status=pending")

            if is_500:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/pending.html")

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=pending&msg={'-'.join(txn.resp_msg.split())}")
        elif txn.status == "TXN_SUCCESS":
            if is_random:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/success.html")

            if is_alumni:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/alumni/index.html?status=success")

            if is_500:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/success.html")

            pay_for = order.pay_for

            if bulk_order:
                users = txn.users

                for user in users:
                    if pay_for == "pass-499.00":
                        user.amount_paid = True
                        user.pronites = True
                        user.main_pronite = True
                        user.igmun = False
                    elif pay_for == "pass-799.00":
                        user.amount_paid = True
                        user.pronites = True
                        user.main_pronite = True
                        user.igmun = False
                        user.is_gold = True
                    elif pay_for == "gold-upgrade":
                        user.is_gold = True
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
                    elif pay_for == "pass-1500.00-upgrade":
                        user.igmun = True
                    elif pay_for == "pass-2500.00-upgrade":
                        user.igmun = True
                        user.accomodation_4 = False
                        user.accomodation_2 = True
                    elif pay_for == "pass-2500.00":
                        user.amount_paid = True
                        user.pronites = True
                        user.main_pronite = True
                        user.igmun = True
                        user.accomodation_2 = True
                    elif pay_for == "pass-1800.00":
                        user.accomodation_4 = True
                    elif pay_for == "pass-1000.00":
                        user.accomodation_2 = True
                    elif pay_for == "pass-1499.00-antarang":
                        if user.amount_paid is True:
                            user.flagship = True
                            user.antarang = True
                            event = Event.objects.get(name='Antarang')
                            user.events_registered.add(event)
                            user.save()
                            team = TeamRegistration.objects.create(
                                leader=user,
                                event=event
                            )
                            team.save()
                    elif pay_for == "pass-1499.00-nrityansh":
                        if user.amount_paid is True:
                            user.flagship = True
                            user.nrityansh = True
                            event = Event.objects.get(name='Nrityansh')
                            user.events_registered.add(event)
                            user.save()
                            team = TeamRegistration.objects.create(
                                leader=user,
                                event=event
                            )
                            team.save()
                    elif pay_for == "pass-1499.00-aayaam":
                        if user.amount_paid is True:
                            user.flagship = True
                            user.aayaam = True
                            event = Event.objects.get(name='Aayaam')
                            user.events_registered.add(event)
                            user.save()
                            team = TeamRegistration.objects.create(
                                leader=user,
                                event=event
                            )
                            team.save()
                    elif pay_for == "pass-1499.00-clashofbands":
                        if user.amount_paid is True:
                            user.flagship = True
                            user.cob = True
                            event = Event.objects.get(name='Thunder Beats')
                            user.events_registered.add(event)
                            user.save()
                            team = TeamRegistration.objects.create(
                                leader=user,
                                event=event
                            )
                            team.save()
                    elif pay_for == "pass-200.00-dance-workshop":
                        event = Event.objects.get(name='Dance Workshop')
                        user.events_registered.add(event)
                    elif pay_for == "pass-129.00-resinart-workshop":
                        event = Event.objects.get(name='Resin Art Workshop')
                        user.events_registered.add(event)
                    elif pay_for == "pass-100.00-music-workshop":
                        event = Event.objects.get(name='Music Workshop')
                        user.events_registered.add(event)
                    elif pay_for == "pass-100.00-filmmaking-workshop":
                        event = Event.objects.get(name='Film Making Workshop')
                        user.events_registered.add(event)
                    elif pay_for == "pass-150.00-pottery-workshop":
                        event = Event.objects.get(name='Pottery Workshop')
                        user.events_registered.add(event)
                    elif pay_for == "pass-150.00-phadpainting-workshop":
                        event = Event.objects.get(name='Phad Painting Workshop')
                        user.events_registered.add(event)
                    elif pay_for == "pass-150.00-papercutting-workshop":
                        event = Event.objects.get(name='Paper Cutting Workshop')
                        user.events_registered.add(event)
                    user.save()
            else:
                user = txn.user

                if order.promo_code:
                    order.promo_code.use()
                if pay_for == "pass-499.00":
                    user.amount_paid = True
                    user.pronites = True
                    user.main_pronite = True
                    user.igmun = False
                elif pay_for == "pass-799.00":
                    user.amount_paid = True
                    user.pronites = True
                    user.main_pronite = True
                    user.igmun = False
                    user.is_gold = True
                elif pay_for == "gold-upgrade":
                    user.is_gold = True
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
                elif pay_for == "pass-1800.00":
                    user.accomodation_4 = True
                elif pay_for == "pass-1000.00":
                    user.accomodation_2 = True
                elif pay_for == "pass-1499.00-antarang":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.antarang = True
                        event = Event.objects.get(name='Antarang')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()

                        return HttpResponseRedirect(
                            redirect_to=f"{frontend_base_url}/event-details/index.html?ref=antarang&status=success")
                elif pay_for == "pass-1499.00-nrityansh":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.nrityansh = True
                        event = Event.objects.get(name='Nrityansh')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()

                        return HttpResponseRedirect(
                            redirect_to=f"{frontend_base_url}/event-details/index.html?ref=nrityansh&status=success")
                elif pay_for == "pass-1499.00-aayaam":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.aayaam = True
                        event = Event.objects.get(name='Aayaam')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()

                        return HttpResponseRedirect(
                            redirect_to=f"{frontend_base_url}/event-details/index.html?ref=aayaam&status=success")
                elif pay_for == "pass-1499.00-clashofbands":
                    if user.amount_paid is True:
                        user.flagship = True
                        user.cob = True
                        event = Event.objects.get(name='Thunder Beats')
                        user.events_registered.add(event)
                        user.save()
                        team = TeamRegistration.objects.create(
                            leader=user,
                            event=event
                        )
                        team.save()

                        return HttpResponseRedirect(
                            redirect_to=f"{frontend_base_url}/event-details/index.html?ref=clashofbands&status=success")
                elif pay_for == "pass-200.00-dance-workshop":
                    event = Event.objects.get(name='Dance Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=dance-workshop&status=success")
                elif pay_for == "pass-129.00-resinart-workshop":
                    event = Event.objects.get(name='Resin Art Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=resinart-workshop&status=success")
                elif pay_for == "pass-100.00-music-workshop":
                    event = Event.objects.get(name='Music Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=music-workshop&status=success")
                elif pay_for == "pass-100.00-filmmaking-workshop":
                    event = Event.objects.get(name='Film Making Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=filmmaking-workshop&status=success")
                elif pay_for == "pass-150.00-pottery-workshop":
                    event = Event.objects.get(name='Pottery Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=pottery-workshop&status=success")
                elif pay_for == "pass-150.00-phadpainting-workshop":
                    event = Event.objects.get(name='Phad Painting Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=phadpainting-workshop&status=success")
                elif pay_for == "pass-150.00-papercutting-workshop":
                    event = Event.objects.get(name='Paper Cutting Workshop')
                    user.events_registered.add(event)
                    user.save()

                    return HttpResponseRedirect(
                        redirect_to=f"{frontend_base_url}/workshop-details/index.html?ref=papercutting-workshop&status=success")

                user.save()

            if from_app:
                return Response(data={"message": "Payment Success"}, status=status.HTTP_200_OK)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/user-profile/index.html?status=success")
