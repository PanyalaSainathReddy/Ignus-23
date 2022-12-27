from rest_framework import serializers

from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "amount", "amount_paid", "amount_due", "currency", "receipt", "attempts", "timestamp")
