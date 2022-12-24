from django.db import models


class Pass(models.Model):
    PASS_TYPES = (
        ('A', 'Accomodation'),
        ('E', 'Events Participation'),
        ('F', 'Flagship Events'),
        ('N', 'Normal Passes')
    )

    name = models.CharField(max_length=50, default="pass")
    amount = models.IntegerField()
    type = models.CharField(max_length=1, choices=PASS_TYPES, default='N')

    class Meta:
        verbose_name_plural = "Passes"

    def __str__(self) -> str:
        return self.name


class Order(models.Model):
    id = models.CharField(max_length=20, unique=True, primary_key=True)
    user = models.ForeignKey("registration.UserProfile", on_delete=models.DO_NOTHING)
    amount = models.IntegerField()
    amount_paid = models.IntegerField()
    amount_due = models.IntegerField()
    currency = models.CharField(max_length=3, default="INR")
    receipt = models.CharField(max_length=40)
    attempts = models.IntegerField()
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return self.id


class Transaction(models.Model):
    payment_id = models.CharField(max_length=20, unique=True, primary_key=True)
    user = models.ForeignKey("registration.UserProfile", on_delete=models.DO_NOTHING)
    status = models.CharField(max_length=10, default="failed")
    order = models.ForeignKey(Order, on_delete=models.DO_NOTHING)
    signature = models.CharField(max_length=100, blank=True)
    captured = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=False, blank=True)
    contact = models.CharField(max_length=15, blank=True)
    fee = models.IntegerField(blank=True, null=True)
    tax = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField()

    class Meta:
        verbose_name_plural = "Transactions"

    def __str__(self) -> str:
        return self.payment_id

    @property
    def amount(self):
        return self.order.amount_paid
