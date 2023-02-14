import csv
import json

from .models import Order, Transaction
from .utils import id_generator


def convert_to_txn():
    f = open('payments/1675948481555.xls', 'r')
    csv_file = csv.reader(f)
    f.close()

    ids = {}
    dup = []

    for lines in csv_file:
        line = lines[0].split('\t')
        if line[0] == "Category Name":
            continue

        payment_mode = line[1]
        bank_txn_id = line[2]
        timestamp = line[3]
        amount = line[4]
        status = 'TXN_SUCCESS'
        ignus_id = line[6]
        name = line[7]
        email = line[8]
        pay_for = line[10]

        pay_for = pay_for + "; " + name + "; " + email

        if ignus_id in ids:
            dup.append(line)
            continue

        ids[ignus_id] = {
            "payment_mode": payment_mode,
            "bank_txn_id": bank_txn_id,
            "timestamp": timestamp,
            "amount": amount,
            "status": status,
            "name": name,
            "email": email,
            "pay_for": pay_for
        }

    for id in ids:
        order_id = f"IG-SBI-0000-{id_generator(size=18)}"
        user = None
        pay_for = ids[id]["pay_for"]
        amount = ids[id]["amount"]
        response_timestamp = ids[id]["timestamp"]

        order = Order.objects.create(
            id=order_id,
            user=user,
            pay_for=pay_for,
            amount=amount,
            response_timestamp=response_timestamp
        )
        order.save()

        txn_id = id_generator(size=50)
        bank_txn_id = ids[id]["bank_txn_id"]
        status = ids[id]["status"]
        payment_mode = ids[id]["payment_mode"]
        timestamp = ids[id]["timestamp"]

        txn = Transaction.objects.create(
            txn_id=txn_id,
            bank_txn_id=bank_txn_id,
            user=user,
            status=status,
            order=order,
            amount=amount,
            payment_mode=payment_mode,
            timestamp=timestamp
        )
        txn.save()

    dups = {
        "dup": dup
    }
    dups = json.dumps(dup, indent=4)
    f = open("dup_ids.json", "w")
    f.write(dups)
    f.close()
