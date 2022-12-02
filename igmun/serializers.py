from rest_framework import serializers
from .models import EBForm


class EBFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBForm
        fields = ["full_name", "phone_number", "email", "org", "permanent_address", "exp_eb", "exp_delegate", "preferred_comm"]
