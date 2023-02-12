import json
import random
import string

import paytmchecksum
import requests
from django.conf import settings

from .models import Order, Transaction


def id_generator(size=4, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


def get_na_orders():
    na_orders = [order.id for order in Order.objects.all() if order.transaction_set.count() == 0]

    return Order.objects.filter(id__in=na_orders)


def get_pending_transactions():
    return Transaction.objects.filter(status="PENDING").all()


def get_failed_transactions():
    return Transaction.objects.filter(status="TXN_FAILURE").all()


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
