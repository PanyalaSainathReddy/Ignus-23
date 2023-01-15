import datetime
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
import sys
# from .utils import get_referral_code
# from django.conf import settings
from django.middleware import csrf
from rest_framework import exceptions, generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .models import CampusAmbassador, PreCA, PreRegistration, UserProfile, TeamRegistration, Avatar
from .serializers import (CookieTokenRefreshSerializer,
                          PreCARegistrationSerializer,
                          PreRegistrationSerializer, RegisterSerializer,
                          UserProfileSerializer, UserSerializer)
from events.models import Event

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
        user = authenticate(username=username, password=password)
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
            # avatar=request.FILES['avatar'],
            gender=request.data['gender'],
            current_year=request.data['current_year'],
            college=request.data['college'],
            address=request.data['address'],
            state=request.data['state'],
            accommodation_required=request.data['accommodation_required']
        )
        userprofile.save()

        return Response({"message": "User Profile Created Successfully", "uuid": userprofile.uuid}, status=status.HTTP_201_CREATED)

class ImageUpload(generics.CreateAPIView):
    def create(self, request, *args, **kwargs):
        image = request.FILES['image']

        with Image.open(image) as img:
            img.thumbnail((800, 800))
            output = BytesIO()
            img.save(output, format="JPEG", quality=50)
            output.seek(0)
            request.FILES['image'] = InMemoryUploadedFile(output,'ImageField', "%s.jpg" % image.name.split('.')[0], 'image/jpeg', sys.getsizeof(output), None)
        
        image = request.FILES['image']
        print(image)
        a = Avatar.objects.create(
            avatar=image
        )
        a.save()
        print(a.avatar)
        return Response("yo", status=status.HTTP_201_CREATED)


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


class RegisterTeamAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.create(
            leader=leader,
            name = request.data['name'],
            event=Event.objects.get(name=request.data['event'])
        )
        team.save()

        return Response({"message": f"Team {team.name if team.name else ''} Registered Successfully", "team_id": team.id}, status=status.HTTP_201_CREATED)


class AddTeamMembersAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )
        if team.leader != leader:
            return Response("You are not the team leader", status=status.HTTP_403_FORBIDDEN)

        for member in request.data['members']:
            team.members.add(UserProfile.objects.get(registration_code=member))
        
        team.update()

        return Response({"message": "Team Member(s) Added Successfully"}, status=status.HTTP_200_OK)


class DeleteTeamAPIView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )
        if team.leader != leader:
            return Response("You are not the team leader", status=status.HTTP_403_FORBIDDEN)
        
        team.delete()

        return Response({"message": "Team Deleted Successfully"}, status=status.HTTP_200_OK)


class TeamDetailsAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        leader = UserProfile.objects.get(user=user)
        team = TeamRegistration.objects.get(
            id=request.data['team_id']
        )

        return Response()
