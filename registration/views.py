from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PreRegistrationSerializer, RegisterSerializer, CookieTokenRefreshSerializer, UserSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework import generics, status, exceptions
from .models import UserProfile, PreRegistration, CampusAmbassador
# from .utils import get_referral_code
# from django.conf import settings
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
import datetime


class PreRegistrationAPIView(viewsets.ModelViewSet):
    queryset = PreRegistration.objects.all()
    serializer_class = PreRegistrationSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data
        response = Response()
        username = data.get('email', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)

                response.set_cookie(
                    key='access',
                    value=data["access"],
                    # expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=5), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=False,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=False,
                    httponly=True,
                    samesite='Lax'
                )
                response["X-CSRFToken"] = csrf.get_token(request)
                response.data = {"Success": "Login successfull", "data": data}
                return response
            else:
                return Response({"Not active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.create(
            username=request.data['email'],
            email=request.data['email'],
            first_name=request.data['first_name'],
            last_name=request.data['last_name']
        )

        user.set_password(request.data['password'])
        user.save()

        response = Response()

        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    # expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=5), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=False,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=False,
                    httponly=True,
                    samesite='Lax'
                )

                response["X-CSRFToken"] = csrf.get_token(request)
                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                return Response({"Not active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refreshToken = request.COOKIES.get('refresh')
            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie('access')
            res.delete_cookie('refresh')
            res.delete_cookie("X-CSRFToken")
            res.delete_cookie("csrftoken")
            res["X-CSRFToken"] = None

            return res
        except Exception:
            raise exceptions.ParseError("Invalid token")


class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if request.COOKIES.get("refresh"):
            response.set_cookie(
                key='access',
                value=response.data["access"],
                # expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=5), "%a, %d-%b-%Y %H:%M:%S GMT"),
                secure=False,
                httponly=True,
                samesite='Lax'
            )

            # del response.data["refresh"]
        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)


class UserDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserProfileAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.create(
            user=user,
            phone=request.data['phone'],
            gender=request.data['gender'],
            current_year=request.data['current_year'],
            college=request.data['college'],
            address=request.data['address'],
            state=request.data['state'],
            accommodation_required=request.data['accommodation_required']
        )
        userprofile.save()

        return Response({"message": "User Profile Created Successfully", "uuid": userprofile.uuid}, status=status.HTTP_201_CREATED)


class UserProfileDetailsView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(user=user)
        userserializer = UserSerializer(user)
        userprofileserializer = UserProfileSerializer(userprofile)

        return Response({"user": userserializer.data, "userprofile": userprofileserializer.data})


class CARegisterAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(user=user)
        ca = CampusAmbassador.objects.create(
            ca_user=userprofile,
        )
        ca.save()

        return Response({"message": "CA Registered Successfully", "referral_code": ca.referral_code}, status=status.HTTP_201_CREATED)
