import json
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

from .models import (AlumniConfirmPresence, AlumniContribution, BulkOrder,
                     BulkTransaction, Order, PromoCode, Transaction)
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


@api_view(['POST'])
def confirm_alumni_presence(request):
    data = request.data

    acp = AlumniConfirmPresence.objects.create(
        name=data.get('name'),
        passing_year=data.get('passing_year'),
        email=data.get('email'),
        phone=data.get('phone')
    )
    acp.save()

    return Response(data={"message": "Your Presence is Confirmed"}, status=status.HTTP_201_CREATED)


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

        if promo_code:
            try:
                promo = PromoCode.objects.get(code=promo_code)

                if pay_for == promo.pass_name:
                    if promo.is_valid():
                        amount = promo.discounted_amount
                        promo.use()
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
        order.users.add(UserProfile.objects.get(registration_code=user_id))
    order.save()

    link = f"https://ignus.co.in/payments/pay.html?mid={mid}&orderId={order_id}&txnToken={txnToken}"
    return HttpResponseRedirect(redirect_to=link)


@api_view(['POST'])
def alumni_contribute(request):
    ac = AlumniContribution.objects.create(
        name=request.data.get('name'),
        passing_year=request.data.get('passing_year'),
        email=request.data.get('email'),
        phone=request.data.get('phone'),
        amount=request.data.get('amount'),
        remarks=request.data.get('remarks', '')
    )
    ac.save()

    timestamp = round(time() * 1000)
    rand = id_generator()
    ignus_id = "IG-ALU-0000"
    order_id = ignus_id+"-"+str(timestamp)+"-"+rand
    callback_url = "https://api.ignus.co.in/api/payments/callback/"
    mid = settings.PAYTM_MID
    merchant_key = settings.PAYTM_MERCHANT_KEY
    amount = request.data.get('amount')
    remarks = request.data.get('remarks', '')
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
            "firstName": request.data.get('name').split()[0],
            "lastName": request.data.get('name').split()[1]
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
        pay_for=remarks,
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

    print("Updating NA Orders...")
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

    print("Updating Pending Transactions...")
    for t in pending_txns:
        data = get_payment_status(t.order.id)
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
        order_id = txn.order.id
        if order_id[:11] == "IG-RAN-0000" or order_id[:11] == "IG-ALU-0000":
            pass
        else:
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

        is_random = order_id[:11] == "IG-RAN-0000"
        is_alumni = order_id[:11] == "IG-ALU-0000"
        bulk_order = order_id[:11] == "IG-BUL-0000"

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
            # print("Checksum Mismatched")

            if from_app:
                return Response(data={"message": "Invalid Payment"}, status=status.HTTP_400_BAD_REQUEST)

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed")

        # print("Checksum Matched")

        if txn.status == "TXN_FAILURE":
            # send_mail(txn)

            if from_app:
                return Response(data={"message": txn.resp_msg}, status=status.HTTP_400_BAD_REQUEST)

            if is_random or bulk_order:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/failed.html")

            if is_alumni:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}")

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=failed&msg={'-'.join(txn.resp_msg.split())}")
        elif txn.status == "PENDING":
            # send_mail(txn)

            if from_app:
                return Response(data={"message": txn.resp_msg}, status=status.HTTP_400_BAD_REQUEST)

            if is_random or bulk_order:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/pending.html")

            if is_alumni:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}")

            return HttpResponseRedirect(
                redirect_to=f"{frontend_base_url}/payment_steps/steps.html?status=pending&msg={'-'.join(txn.resp_msg.split())}")
        elif txn.status == "TXN_SUCCESS":
            if is_random:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/payments/success.html")

            if is_alumni:
                return HttpResponseRedirect(redirect_to=f"{frontend_base_url}")

            pay_for = order.pay_for

            if bulk_order:
                users = txn.users

                for user in users:
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

                    user.save()
            else:
                user = txn.user
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

                user.save()

            # send_mail(txn)

            if from_app:
                return Response(data={"message": "Payment Success"}, status=status.HTTP_200_OK)

            return HttpResponseRedirect(redirect_to=f"{frontend_base_url}/user-profile/index.html?status=success")
