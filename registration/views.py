from django.urls import reverse
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, RegisterSerializer, UserProfileSerializer, PreRegistrationSerializer
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework import generics, status
from .models import UserProfile, PreRegistration
import requests
# from .utils import get_referral_code


class PreRegistrationAPIView(generics.CreateAPIView):
    serializer_class = PreRegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        prereg = PreRegistration.objects.create(
            full_name=request.data['full_name'],
            email=request.data['email'],
            phone_number=request.data['phone_number'],
            college=request.data['college'],
            college_state=request.data['college_state'],
            current_year=request.data['current_year'],
            gender=request.data['gender'],
            por=request.data['por'],
            por_holder_contact=request.data['por_holder_contact']
        )
        prereg.save()

        return Response({"message": "Pre-Registration Successful"}, status=status.HTTP_201_CREATED)


class UserDetailAPI(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

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
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        user = User.objects.get(id=request.user.id)
        userprofile = UserProfile.objects.get(user=user)
        userserializer = UserSerializer(user)
        userprofileserializer = UserProfileSerializer(userprofile)

        return Response({"user": userserializer.data, "userprofile": userprofileserializer.data})


# class CARegisterAPIView(generics.CreateAPIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated,)
#     serializer_class = CASerializer

#     def create(self, request, *args, **kwargs):
#         user = User.objects.get(id=request.user.id)
#         userprofile = UserProfile.objects.get(user=user)
#         ca = CampusAmbassador.objects.create(
#             ca_user=userprofile,
#             insta_link=request.data['insta_link'],
#             workshop_capability=request.data['workshop_capability'],
#             publicize_ignus=request.data['publicize_ignus'],
#             past_experience=request.data['past_experience'],
#             description=request.data['description'],
#             referral_code=get_referral_code()
#         )
#         ca.save()

#         return Response({"message": "CA Registered Successfully", "referral_code": ca.referral_code}, status=status.HTTP_201_CREATED)
