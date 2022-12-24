from rest_framework import viewsets, serializers
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
from urllib.parse import urlencode
from django.shortcuts import redirect
from .utils import google_get_access_token, google_get_user_info


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
        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)

                response.set_cookie(
                    key='access',
                    value=data["access"],
                    # expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=False,
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
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=False,
                    samesite='Lax'
                )
                response["X-CSRFToken"] = csrf.get_token(request)
                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                return Response({"Not active": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Invalid": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


class GoogleRegisterView(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = 'http://127.0.0.1:5500/frontend/login.html'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = 'http://127.0.0.1:8000/api/accounts/register/google/'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        user = User.objects.create(
            username=user_data['email'],
            email=user_data['email'],
            first_name=user_data.get('given_name', ''),
            last_name=user_data.get('family_name', ''),
        )

        user.set_password('google')
        user.save()

        response = Response(status=302)

        user = authenticate(username=user_data['email'], password='google')
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    # expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=False,
                    samesite='Lax'
                )
                response["X-CSRFToken"] = csrf.get_token(request)
                response['Location'] = 'http://127.0.0.1:5500/frontend/complete-profile/index.html'
                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                response.data = {"Not active": "This account is not active!!"}
                # response.status_code = status.HTTP_404_NOT_FOUND
                response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
                return response
        else:
            response.data = {"Invalid": "Invalid username or password!!"}
            # response.status_code = status.HTTP_404_NOT_FOUND
            response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
            return response


class GoogleLoginView(APIView):
    class InputSerializer(serializers.Serializer):
        code = serializers.CharField(required=False)
        error = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get('code')
        error = validated_data.get('error')

        login_url = 'http://127.0.0.1:5500/frontend/login.html'

        if error or not code:
            params = urlencode({'error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = 'http://127.0.0.1:8000/api/accounts/login/google/'

        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        user_data = google_get_user_info(access_token=access_token)
        response = Response(status=302)

        user = authenticate(username=user_data['email'], password='google')
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    # expires=settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    # expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=False,
                    samesite='Lax'
                )
                response["X-CSRFToken"] = csrf.get_token(request)
                response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
                response.data = {"Success": "Login successfull", "data": data}
                return response
            else:
                response.data = {"Not active": "This account is not active!!"}
                # response.status_code = status.HTTP_404_NOT_FOUND
                response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
                return response
        else:
            response.data = {"Invalid": "You are not registered!!"}
            # response.status_code = status.HTTP_404_NOT_FOUND
            response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
            return response


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
            res.delete_cookie('LoggedIn')
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
                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                secure=True,
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
            state=request.data['state'],
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
