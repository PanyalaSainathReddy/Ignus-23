import datetime
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
# from django.middleware import csrf
from django.shortcuts import redirect
from rest_framework import exceptions, generics, serializers, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import CampusAmbassador, PreCA, PreRegistration, UserProfile
from .serializers import (CookieTokenRefreshSerializer,
                          PreCARegistrationSerializer,
                          PreRegistrationSerializer, RegisterSerializer,
                          UserProfileSerializer, UserSerializer)
from .utils import google_get_access_token, google_get_user_info

# from igmun.models import IGMUNCampusAmbassador

User = get_user_model()


class PreRegistrationAPIView(viewsets.ModelViewSet):
    queryset = PreRegistration.objects.all()
    serializer_class = PreRegistrationSerializer


class PreCARegistrationAPIView(viewsets.ModelViewSet):
    queryset = PreCA.objects.all()
    serializer_class = PreCARegistrationSerializer


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
                        response.set_cookie(
                            key='access',
                            value=data["access"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='refresh',
                            value=data["refresh"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=True,
                            samesite='Lax'
                        )

                        # response.set_cookie(
                        #     key='csrftoken',
                        #     value=csrf.get_token(request),
                        #     expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                        #     secure=True,
                        #     domain=".ignus.co.in",
                        #     httponly=False,
                        #     samesite='Lax'
                        # )

                        response.set_cookie(
                            key='LoggedIn',
                            value=True,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=False,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='isProfileComplete',
                            value=user.profile_complete,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=False,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='isGoogle',
                            value=user.is_google,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=False,
                            samesite='Lax'
                        )
                        if user.profile_complete:
                            userprofile = UserProfile.objects.get(user=user)
                            response.set_cookie(
                                key='isCA',
                                value=userprofile.is_ca,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=True,
                                domain=".ignus.co.in",
                                httponly=False,
                                samesite='Lax'
                            )
                            response.set_cookie(
                                key='ignusID',
                                value=userprofile.registration_code,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=True,
                                domain=".ignus.co.in",
                                httponly=False,
                                samesite='Lax'
                            )

                        # response["X-CSRFToken"] = csrf.get_token(request)
                        response.data = {"Success": "Login successfull", "data": data}
                        return response
                    else:
                        return Response({"Error": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
                else:
                    return Response({"Error": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Error": "User does not exist, please Signup!!"}, status=status.HTTP_404_NOT_FOUND)


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
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=True,
                    samesite='Lax'
                )

                # response.set_cookie(
                #     key='csrftoken',
                #     value=csrf.get_token(request),
                #     expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                #     secure=True,
                #     domain=".ignus.co.in",
                #     httponly=False,
                #     samesite='Lax'
                # )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isProfileComplete',
                    value=user.profile_complete,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isGoogle',
                    value=user.is_google,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=False,
                    samesite='Lax'
                )

                if user.profile_complete:
                    userprofile = UserProfile.objects.get(user=user)
                    response.set_cookie(
                        key='isCA',
                        value=userprofile.is_ca,
                        expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                        secure=True,
                        domain=".ignus.co.in",
                        httponly=False,
                        samesite='Lax'
                    )
                    response.set_cookie(
                        key='ignusID',
                        value=userprofile.registration_code,
                        expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                        secure=True,
                        domain=".ignus.co.in",
                        httponly=False,
                        samesite='Lax'
                    )

                # response["X-CSRFToken"] = csrf.get_token(request)
                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                return Response({"Error": "This account is not active!!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"Error": "Invalid username or password!!"}, status=status.HTTP_404_NOT_FOUND)


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

        login_url = 'https://ignus.co.in/login.html'

        if error or not code:
            params = urlencode({'Error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = 'https://api.ignus.co.in/api/accounts/register/google/'

        try:
            access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        except Exception:
            params = urlencode({'Error': "Failed to obtain access token from Google."})
            return redirect(f'{login_url}?{params}')

        try:
            user_data = google_get_user_info(access_token=access_token)
        except Exception:
            params = urlencode({'Error': "Failed to obtain user info from Google."})
            return redirect(f'{login_url}?{params}')

        try:
            user = User.objects.create(
                username=user_data['email'],
                email=user_data['email'],
                first_name=user_data.get('given_name', ''),
                last_name=user_data.get('family_name', ''),
                google_picture=user_data.get('picture', ''),
                is_google=True,
            )
            user.set_password('google')
            user.save()
        except Exception:
            params = urlencode({'Error': "User already exists, try to sign-in!"})
            return redirect(f'{login_url}?{params}')

        response = Response(status=302)
        user = authenticate(username=user_data['email'], password='google')
        if user is not None:
            if user.is_active:
                data = get_tokens_for_user(user)
                response.set_cookie(
                    key='access',
                    value=data["access"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=True,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='refresh',
                    value=data["refresh"],
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=True,
                    samesite='Lax'
                )

                # response.set_cookie(
                #     key='csrftoken',
                #     value=csrf.get_token(request),
                #     expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                #     secure=True,
                #     domain=".ignus.co.in",
                #     httponly=False,
                #     samesite='Lax'
                # )

                response.set_cookie(
                    key='LoggedIn',
                    value=True,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isProfileComplete',
                    value=user.profile_complete,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=False,
                    samesite='Lax'
                )

                response.set_cookie(
                    key='isGoogle',
                    value=user.is_google,
                    expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                    secure=True,
                    domain=".ignus.co.in",
                    httponly=False,
                    samesite='Lax'
                )

                if user.profile_complete:
                    userprofile = UserProfile.objects.get(user=user)
                    response.set_cookie(
                        key='isCA',
                        value=userprofile.is_ca,
                        expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                        secure=True,
                        domain=".ignus.co.in",
                        httponly=False,
                        samesite='Lax'
                    )
                    response.set_cookie(
                        key='ignusID',
                        value=userprofile.registration_code,
                        expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                        secure=True,
                        domain=".ignus.co.in",
                        httponly=False,
                        samesite='Lax'
                    )

                # response["X-CSRFToken"] = csrf.get_token(request)
                response['Location'] = 'https://ignus.co.in/complete-profile/index.html'
                response.data = {"Success": "Registration successfull", "data": data}
                return response
            else:
                params = urlencode({'Error': "This account is not active!!"})
                return redirect(f'{login_url}?{params}')
        else:
            params = urlencode({'Error': "Invalid username or password!!"})
            return redirect(f'{login_url}?{params}')


class GoogleRegisterViewApp(APIView):
    def post(self, request, format=None):
        secret = settings.APP_SECRET
        incoming_secret = request.headers.get('X-App')

        if secret != incoming_secret:
            return Response(data={"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        try:
            user = User.objects.create(
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                email=data.get('email'),
                username=data.get('email'),
                google_picture=data.get('picture', ''),
                is_google=True
            )
        except Exception:
            return Response(data={"message": "User Already Exists"}, status=status.HTTP_409_CONFLICT)

        user.set_password('google')
        user.save()

        user = authenticate(username=data.get('email'), password='google')

        if user is None:
            return Response(data={"message": "Username or Password Invalid"}, status=status.HTTP_404_NOT_FOUND)

        data = get_tokens_for_user(user)
        # csrftoken = csrf.get_token(request=request)

        res = Response(
            data={
                "message": "Registration Successful",
                "access": data["access"],
                "refresh": data["refresh"],
                # "csrftoken": csrftoken,
            },
            status=status.HTTP_201_CREATED
        )
        # res['X-CSRFToken'] = csrftoken

        return res


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

        login_url = 'https://ignus.co.in/login.html'

        if error or not code:
            params = urlencode({'Error': error})
            return redirect(f'{login_url}?{params}')

        redirect_uri = 'https://api.ignus.co.in/api/accounts/login/google/'

        try:
            access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)
        except Exception:
            params = urlencode({'Error': "Failed to obtain access token from Google."})
            return redirect(f'{login_url}?{params}')

        try:
            user_data = google_get_user_info(access_token=access_token)
        except Exception:
            params = urlencode({'Error': "Failed to obtain user info from Google."})
            return redirect(f'{login_url}?{params}')

        response = Response(status=302)

        if User.objects.filter(email=user_data['email']).exists():
            if User.objects.get(email=user_data['email']).is_google:
                user = authenticate(username=user_data['email'], password='google')
                if user is not None:
                    if user.is_active:
                        data = get_tokens_for_user(user)
                        response.set_cookie(
                            key='access',
                            value=data["access"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=True,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='refresh',
                            value=data["refresh"],
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=True,
                            samesite='Lax'
                        )

                        # response.set_cookie(
                        #     key='csrftoken',
                        #     value=csrf.get_token(request),
                        #     expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                        #     secure=True,
                        #     domain=".ignus.co.in",
                        #     httponly=False,
                        #     samesite='Lax'
                        # )

                        response.set_cookie(
                            key='LoggedIn',
                            value=True,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=False,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='isProfileComplete',
                            value=user.profile_complete,
                            expires=datetime.datetime.strftime(datetime.datetime.now() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=False,
                            samesite='Lax'
                        )

                        response.set_cookie(
                            key='isGoogle',
                            value=user.is_google,
                            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                            secure=True,
                            domain=".ignus.co.in",
                            httponly=False,
                            samesite='Lax'
                        )

                        if user.profile_complete:
                            userprofile = UserProfile.objects.get(user=user)
                            response.set_cookie(
                                key='isCA',
                                value=userprofile.is_ca,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=True,
                                domain=".ignus.co.in",
                                httponly=False,
                                samesite='Lax'
                            )
                            response.set_cookie(
                                key='ignusID',
                                value=userprofile.registration_code,
                                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
                                secure=True,
                                domain=".ignus.co.in",
                                httponly=False,
                                samesite='Lax'
                            )
                            response['Location'] = 'https://ignus.co.in/index.html'
                        else:
                            response['Location'] = 'https://ignus.co.in/complete-profile/index.html'
                        # response["X-CSRFToken"] = csrf.get_token(request)
                        response.data = {"Success": "Login successfull", "data": data}
                        return response
                    else:
                        params = urlencode({'Error': "This account is not active!!"})
                        return redirect(f'{login_url}?{params}')
                else:
                    params = urlencode({'Error': "Please Signup first!!"})
                    return redirect(f'{login_url}?{params}')
            else:
                params = urlencode({'Error': "You signed up using email & password!!"})
                return redirect(f'{login_url}?{params}')
        else:
            params = urlencode({'Error': "Please Signup first!!"})
            return redirect(f'{login_url}?{params}')


class GoogleLoginViewApp(APIView):
    def post(self, request, format=None):
        secret = settings.APP_SECRET
        incoming_secret = request.headers.get('X-App')

        if secret != incoming_secret:
            return Response(data={"message": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)

        data = request.data

        if User.objects.filter(email=data.get('email')).exists():
            user = User.objects.get(email=data.get('email'))

            if user.is_google:
                user = authenticate(username=data.get('email'), password='google')

                if user is None:
                    return Response(data={"message": "Username or Password Invalid"}, status=status.HTTP_404_NOT_FOUND)

                data = get_tokens_for_user(user)
                # csrftoken = csrf.get_token(request=request)

                res = Response(
                    data={
                        "message": "Logged In Successfully",
                        "access": data["access"],
                        "refresh": data["refresh"],
                        # "csrftoken": csrftoken,
                    },
                    status=status.HTTP_200_OK
                )
                # res['X-CSRFToken'] = csrftoken

                return res
            else:
                return Response(data={"message": "You signed up using email and password"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            return Response(data={"message": "You need to sign up before you can login"}, status=status.HTTP_406_NOT_ACCEPTABLE)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            refreshToken = request.COOKIES.get('refresh')
            token = RefreshToken(refreshToken)
            token.blacklist()
            res = Response()
            res.delete_cookie('access', domain=".ignus.co.in")
            res.delete_cookie('refresh', domain=".ignus.co.in")
            res.delete_cookie('LoggedIn', domain=".ignus.co.in")
            res.delete_cookie("X-CSRFToken", domain=".ignus.co.in")
            res.delete_cookie("csrftoken", domain=".ignus.co.in")
            res.delete_cookie("isProfileComplete", domain=".ignus.co.in")
            res.delete_cookie("isCA", domain=".ignus.co.in")
            res.delete_cookie("ignusID", domain=".ignus.co.in")
            res.delete_cookie("isGoogle", domain=".ignus.co.in")
            # res["X-CSRFToken"] = None

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
                expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(minutes=30), "%a, %d-%b-%Y %H:%M:%S GMT"),
                secure=True,
                domain=".ignus.co.in",
                httponly=True,
                samesite='Lax'
            )

        # response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response, *args, **kwargs)


class CookieTokenRefreshViewApp(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if request.headers.get("refresh"):
            # response["X-CSRFToken"] = csrf.get_token(request=request)
            pass
        else:
            response.data = {"message": "No Refresh Token Provided"}

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
        referred_by = None

        if referral_code:
            try:
                referred_by = CampusAmbassador.objects.get(referral_code=referral_code)
            except Exception:
                pass

        userprofile = UserProfile.objects.create(
            user=user,
            referred_by=referred_by,
            phone=request.data['phone'],
            # avatar=request.FILES['avatar'],
            gender=request.data['gender'],
            current_year=request.data['current_year'],
            college=request.data['college'],
            state=request.data['state'],
            igmun=request.data["igmun"],
            igmun_pref=request.data["igmun_pref"]
        )
        userprofile.save()

        user.profile_complete = True
        user.save()

        if referred_by:
            if referred_by.number_referred == 20:
                referred_by.verified = True
                referred_by.save()

        response = Response(data={"Message: Profile Created Successfully!"}, status=status.HTTP_201_CREATED)
        # response["X-CSRFToken"] = csrf.get_token(request)

        # max_age = request.COOKIES.get('refresh')
        # print("max_age: ", max_age)
        # expires = datetime.datetime.now() + datetime.timedelta(seconds=max_age)
        # print(expires)
        response.set_cookie(
            key='isProfileComplete',
            value=user.profile_complete,
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=True,
            domain=".ignus.co.in",
            httponly=False,
            samesite='Lax'
        )

        response.set_cookie(
            key='isCA',
            value=userprofile.is_ca,
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=True,
            domain=".ignus.co.in",
            httponly=False,
            samesite='Lax'
        )
        response.set_cookie(
            key='ignusID',
            value=userprofile.registration_code,
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=True,
            domain=".ignus.co.in",
            httponly=False,
            samesite='Lax'
        )

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

        if not userprofile.amount_paid:
            return Response(data={"error": "Please complete your payment before registering for CA."}, status=status.HTTP_402_PAYMENT_REQUIRED)

        ca = CampusAmbassador.objects.create(
            ca_user=userprofile
        )
        ca.save()
        userprofile.is_ca = True
        userprofile.save()

        res = Response({"message": "CA Registered Successfully", "referral_code": ca.referral_code}, status=status.HTTP_201_CREATED)

        res.set_cookie(
            key='isCA',
            value=userprofile.is_ca,
            expires=datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(days=15), "%a, %d-%b-%Y %H:%M:%S GMT"),
            secure=True,
            domain=".ignus.co.in",
            httponly=False,
            samesite='Lax'
        )
        return res
