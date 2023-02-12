import json
from time import time

import paytmchecksum
import requests
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AlumniConfirmPresence, AlumniContribution, Order
from .utils import id_generator


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
    amount = str(request.data.get('amount')) + '.00'
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
            "firstName": request.data.get('name', '')
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

    ac.order = order
    ac.save()

    link = f"https://ignus.co.in/payments/pay.html?mid={mid}&orderId={order_id}&txnToken={txnToken}"
    return Response(
        data={
            "message": "Alumni Order Created Successfully",
            "txnToken": txnToken,
            "orderId": order_id,
            "mid": mid,
            "link": link
        },
        status=status.HTTP_201_CREATED
    )
