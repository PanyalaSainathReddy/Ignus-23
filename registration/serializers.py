from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from .models import UserProfile, PreRegistration


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email"]


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': False}
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["phone", "gender", "current_year", "college", "address", "state", "id_issued", "accommodation_required", "uuid"]


# class CASerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CampusAmbassador
#         fields = ["insta_link", "workshop_capability", "publicize_ignus", "past_experience", "description", "referral_code"]


class PreRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreRegistration
        fields = ["first_name", "last_name", "email", "phone_number", "college", "accomodation_required"]
