from django.core.validators import RegexValidator
from django.db import models


class AlumniConfirmPresence(models.Model):
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')

    name = models.CharField(max_length=200)
    passing_year = models.IntegerField()
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[contact])

    class Meta:
        verbose_name_plural = "Alumni Confirm Presence"

    def __str__(self) -> str:
        return self.name


class AlumniContribution(models.Model):
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')

    name = models.CharField(max_length=200, unique=False)
    passing_year = models.IntegerField(unique=False)
    email = models.EmailField(unique=False)
    amount = models.IntegerField(unique=False)
    phone = models.CharField(max_length=10, validators=[contact], unique=False)
    remarks = models.CharField(max_length=1000, unique=False)

    class Meta:
        verbose_name_plural = "Alumni Contributions"

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    user = models.ForeignKey("registration.UserProfile", on_delete=models.DO_NOTHING, null=True, blank=True)
    checksum = models.CharField(max_length=200, default="")
    pay_for = models.CharField(max_length=100, default="")
    amount = models.CharField(max_length=10, default="1.00")
    currency = models.CharField(max_length=3, default="INR")
    request_timestamp = models.CharField(max_length=20, default="")
    signature = models.CharField(max_length=200, default="")
    response_timestamp = models.CharField(max_length=20, default="")
    result_code = models.CharField(max_length=4, default="0000")
    result_msg = models.CharField(max_length=200, default="")
    transaction_token = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.id

    def transacted(self):
        if self.transaction_set.count() > 0:
            return True
        return False

    def transaction_status(self):
        if self.transacted():
            return self.transaction_set.all()[0].status
        return "NA"

    def is_random(self):
        return self.id[:11] == "IG-RAN-0000"


class BulkOrder(models.Model):
    id = models.CharField(max_length=30, unique=True, primary_key=True)
    users = models.ManyToManyField("registration.UserProfile", blank=True)
    checksum = models.CharField(max_length=200, default="")
    pay_for = models.CharField(max_length=100, default="")
    amount = models.CharField(max_length=10, default="1.00")
    currency = models.CharField(max_length=3, default="INR")
    request_timestamp = models.CharField(max_length=20, default="")
    signature = models.CharField(max_length=200, default="")
    response_timestamp = models.CharField(max_length=20, default="")
    result_code = models.CharField(max_length=4, default="0000")
    result_msg = models.CharField(max_length=200, default="")
    transaction_token = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name_plural = "Bulk Orders"

    def __str__(self):
        return self.id

    def transacted(self):
        if self.transaction_set.count() > 0:
            return True
        return False

    def transaction_status(self):
        if self.transacted():
            return self.transaction_set.all()[0].status
        return "NA"


class Transaction(models.Model):
    txn_id = models.CharField(max_length=100, unique=True, primary_key=True, default="")
    bank_txn_id = models.CharField(max_length=100, default="")
    user = models.ForeignKey("registration.UserProfile", on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.CharField(max_length=100, default="failed")
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    amount = models.CharField(max_length=10, default="1.00")
    gateway_name = models.CharField(max_length=20, default="")
    payment_mode = models.CharField(max_length=20, default="UPI")
    resp_code = models.CharField(max_length=5, default="")
    resp_msg = models.CharField(max_length=200, default="")
    timestamp = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name_plural = "Transactions"
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return self.txn_id


class BulkTransaction(models.Model):
    txn_id = models.CharField(max_length=100, unique=True, primary_key=True, default="")
    bank_txn_id = models.CharField(max_length=100, default="")
    users = models.ManyToManyField("registration.UserProfile", blank=True)
    status = models.CharField(max_length=100, default="failed")
    order = models.ForeignKey(BulkOrder, on_delete=models.DO_NOTHING)
    amount = models.CharField(max_length=10, default="1.00")
    gateway_name = models.CharField(max_length=20, default="")
    payment_mode = models.CharField(max_length=20, default="UPI")
    resp_code = models.CharField(max_length=5, default="")
    resp_msg = models.CharField(max_length=200, default="")
    timestamp = models.CharField(max_length=100, default="")

    class Meta:
        verbose_name_plural = "Bulk Transactions"
        ordering = ['-timestamp']

    def __str__(self) -> str:
        return self.txn_id


class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, primary_key=True)
    pass_name = models.CharField(max_length=100, default='')
    discounted_amount = models.CharField(max_length=10, default='0.00')
    max_uses = models.IntegerField(default=1)
    uses = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Promo Codes"

    def __str__(self) -> str:
        return self.code

    def is_valid(self):
        if self.valid and self.uses < self.max_uses:
            return True
        return False

    def use(self):
        self.uses += 1
        self.save()
