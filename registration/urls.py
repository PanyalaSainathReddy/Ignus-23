from django.urls import path, include
from rest_framework import routers
from .views import UserDetailAPI, RegisterUserAPIView, UserProfileAPIView, UserProfileDetailsView, PreRegistrationAPIView

router = routers.DefaultRouter()
router.register(r'pre-register', PreRegistrationAPIView)
urlpatterns = [
    path("user-details/", UserDetailAPI.as_view()),
    path('register/', RegisterUserAPIView.as_view()),
    path('user-profile/', UserProfileAPIView.as_view()),
    path('user-profile-details/', UserProfileDetailsView.as_view()),
    # path('ca-register/', CARegisterAPIView.as_view()),
    # path('pre-register/', PreRegistrationAPIView)
    path('', include(router.urls)),
]
