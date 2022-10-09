from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from .models import UserProfile


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
