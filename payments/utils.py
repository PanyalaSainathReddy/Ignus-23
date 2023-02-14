import json
import random
import string

import paytmchecksum
import requests
from django.conf import settings

from events.models import Event, TeamRegistration

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


def update_failed_payments():
    failed_txns = get_failed_transactions()
    updated_transactions = []

    print("Updating Failed Transactions...")
    for t in failed_txns:
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
