from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from .models import UserProfile, PreRegistration, PreCA
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

User = get_user_model()


class PreRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreRegistration
        fields = ["full_name", "email", "phone_number", "college", "college_state", "current_year", "por", "por_holder_contact"]


class PreCARegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreCA
        fields = ["full_name", "email", "phone_number", "college", "city", "college_state", "current_year"]


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


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise exceptions.ParseError(
                'No valid token found in cookie \'refresh\'')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "google_picture", "is_google", "profile_complete"]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["referred_by", "user", "profile_pic", "phone", "gender", "current_year", "college", "state", "registration_code", "is_ca", "amount_paid", "pronites", "igmun", "accomodation", "main_pronite",
                  "flagship", "igmun_pref", "qr_code", "pronites_qr"]
