from django.urls import reverse
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from .models import UserProfile
import requests


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        serializer = UserSerializer(user)
        return Response(serializer.data)


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

        r = requests.post(
            url=request.build_absolute_uri(reverse('login')),
            data={
                'username': request.data['email'],
                'password': request.data['password']
            }
        )

        res = {
            'message': 'User created successfully',
            'token': r.json()['token'],
            'email': user.email
        }

        return Response(res, status=status.HTTP_201_CREATED)


class UserProfileAPIView(generics.CreateAPIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
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
    authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(user=user)
        userserializer = UserSerializer(user)
        userprofileserializer = UserProfileSerializer(userprofile)

        return Response({"user": userserializer.data, "userprofile": userprofileserializer.data})
