from rest_framework import viewsets, serializers
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import PreRegistrationSerializer, RegisterSerializer, CookieTokenRefreshSerializer, UserSerializer, UserProfileSerializer
from django.contrib.auth import get_user_model
from rest_framework import generics, status, exceptions
from .models import UserProfile, PreRegistration, CampusAmbassador
from igmun.models import IGMUNCampusAmbassador
from payments.models import Pass, Order
from django.middleware import csrf
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth import authenticate
import datetime
from urllib.parse import urlencode
from django.shortcuts import redirect
from .utils import google_get_access_token, google_get_user_info
from payments.utils import setupRazorpay
# from payments.serializers import OrderSerializer

User = get_user_model()


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

        if User.objects.filter(username=username).exists():
            if User.objects.filter(username=username).first().is_google:
                return Response({"Error": "Please use Google Login"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user = authenticate(username=username, password=password)
                if user is not None:
                    if user.is_active:
                        data = get_tokens_for_user(user)
                        if user.profile_complete:
                            userprofile = UserProfile.objects.get(user=user)
                            order = Order.objects.get(user=userprofile)
                            response.set_cookie(
                                key='order_id',
                                value=order.id,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=False,
                                httponly=False,
                                samesite='Lax'
                            )
                            response.set_cookie(
                                key='amount_due',
                                value=order.amount_due * 100,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=False,
                                httponly=False,
                                samesite='Lax'
                            )
                            response.set_cookie(
                                key='currency',
                                value=order.currency,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=False,
                                httponly=False,
                                samesite='Lax'
                            )

                        response.set_cookie(
                            key='access',
                            value=data["access"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='refresh',
                            value=data["refresh"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='LoggedIn',
                            value=True,
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
        else:
            return Response({"Error": "User does not exist, please register!!"}, status=status.HTTP_404_NOT_FOUND)


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = User.objects.create(
                username=request.data['email'],
                email=request.data['email'],
                first_name=request.data['first_name'],
                last_name=request.data['last_name']
            )

            user.set_password(request.data['password'])
            user.save()
        except Exception:
            return Response({"Error": "User already exists, try to sign-in!!"}, status=status.HTTP_409_CONFLICT)

        response = Response()

        user = authenticate(username=request.data['email'], password=request.data['password'])
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
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
        response = Response(status=302)

        try:
            user = User.objects.create(
                username=user_data['email'],
                email=user_data['email'],
                first_name=user_data.get('given_name', ''),
                last_name=user_data.get('family_name', ''),
                is_google=True,
            )
            user.set_password('google')
            user.save()
        except Exception:
            response.data = {"Error": "User already exists, try to sign-in!"}
            response['Location'] = 'http://127.0.0.1:5500/frontend/login.html'
            return response

        user = authenticate(username=user_data['email'], password='google')
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
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
                response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
                return response
        else:
            response.data = {"Invalid": "Invalid username or password!!"}
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

        if User.objects.filter(email=user_data['email']).exists():
            if User.objects.get(email=user_data['email']).is_google:
                user = authenticate(username=user_data['email'], password='google')
                if user is not None:
                    if user.is_active:
                        data = get_tokens_for_user(user)

                        if user.profile_complete:
                            userprofile = UserProfile.objects.get(user=user)
                            order = Order.objects.get(user=userprofile)
                            response.set_cookie(
                                key='order_id',
                                value=order.id,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=False,
                                httponly=False,
                                samesite='Lax'
                            )
                            response.set_cookie(
                                key='amount_due',
                                value=order.amount_due * 100,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=False,
                                httponly=False,
                                samesite='Lax'
                            )
                            response.set_cookie(
                                key='currency',
                                value=order.currency,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=False,
                                httponly=False,
                                samesite='Lax'
                            )

                        response.set_cookie(
                            key='access',
                            value=data["access"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='refresh',
                            value=data["refresh"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='LoggedIn',
                            value=True,
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
                        response['Location'] = 'http://127.0.0.1:5500/frontend/index.html'
                        return response
                else:
                    response.data = {"Invalid": "You are not registered!!"}
                    response['Location'] = 'http://127.0.0.1:5500/frontend/login.html'
                    return response
            else:
                response.data = {"Invalid": "You signed up using email!!"}
                response['Location'] = 'http://127.0.0.1:5500/frontend/login.html'
                return response
        else:
            response.data = {"Invalid": "You are not registered!!"}
            response['Location'] = 'http://127.0.0.1:5500/frontend/login.html'
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
                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                secure=True,
                httponly=True,
                samesite='Lax'
            )

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
        referral_code = request.data["referral_code"]
        referral_code_igmun = request.data["referral_code_igmun"]
        referred_by = None
        referred_by_igmun = None

        p = request.data["pass"]
        p = Pass.objects.get(name=p)

        if referral_code_igmun:
            referred_by_igmun = IGMUNCampusAmbassador.objects.get(referral_code=referral_code_igmun)
        else:
            if referral_code:
                referred_by = CampusAmbassador.objects.get(referral_code=referral_code)

        userprofile = UserProfile.objects.create(
            user=user,
            referred_by=referred_by,
            referred_by_igmun=referred_by_igmun,
            phone=request.data['phone'],
            gender=request.data['gender'],
            current_year=request.data['current_year'],
            college=request.data['college'],
            state=request.data['state'],
            igmun=request.data["igmun"]
        )
        userprofile._pass.add(p)
        userprofile.save()

        user.profile_complete = True
        user.save()

        if referred_by_igmun:
            if referred_by_igmun.number_referred == 20:
                referred_by_igmun.verified = True
                referred_by_igmun.save()
        else:
            if referred_by:
                if referred_by.number_referred == 20:
                    referred_by.verified = True
                    referred_by.save()

        rzpClient = setupRazorpay()
        numOrders = Order.objects.count()
        data = {
            "amount": userprofile.amount_due * 100,
            "currency": "INR",
            "receipt": f"order_rcptid_{numOrders+1}"
        }
        paymentOrder = rzpClient.order.create(data=data)
        paymentOrder["created_at"] = datetime.datetime.fromtimestamp(paymentOrder["created_at"])

        Order.objects.create(
            id=paymentOrder["id"],
            user=userprofile,
            amount=paymentOrder["amount"] // 100,
            amount_paid=paymentOrder["amount_paid"] // 100,
            amount_due=paymentOrder["amount_due"] // 100,
            currency=paymentOrder["currency"],
            receipt=paymentOrder["receipt"],
            attempts=paymentOrder["attempts"],
            timestamp=paymentOrder["created_at"]
        )

        response = Response(data={"Message: Profile Created Successfully!"}, status=status.HTTP_201_CREATED)
        response.set_cookie(
            key='order_id',
            value=paymentOrder["id"],
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=False,
            httponly=False,
            samesite='Lax'
        )
        response.set_cookie(
            key='amount_due',
            value=paymentOrder["amount_due"],
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=False,
            httponly=False,
            samesite='Lax'
        )
        response.set_cookie(
            key='currency',
            value=paymentOrder["currency"],
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=False,
            httponly=False,
            samesite='Lax'
        )
        response["X-CSRFToken"] = csrf.get_token(request)

        return response


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
            ca_user=userprofile
        )
        ca.save()

        userprofile.is_ca = True
        userprofile.save()

        return Response({"message": "CA Registered Successfully", "referral_code": ca.referral_code}, status=status.HTTP_201_CREATED)
