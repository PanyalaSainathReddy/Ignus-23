from rest_framework import serializers

from .models import EBForm, PreRegistrationForm


class EBFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = EBForm
        fields = ["full_name", "phone_number", "email", "org", "city", "exp_eb", "exp_delegate", "preferred_comm1", "preferred_comm2", "preferred_comm3"]


class PreRegistrationFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreRegistrationForm
        fields = ["full_name", "phone_number", "email", "org", "city", "exp_delegate", "preferred_comm1", "preferred_comm2", "preferred_comm3"]
