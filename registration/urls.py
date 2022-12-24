from django.urls import path, include
from rest_framework import routers
from .views import UserDetailAPI, RegisterUserAPIView, UserProfileAPIView, UserProfileDetailsView, PreRegistrationAPIView, LoginView, LogoutView, CookieTokenRefreshView, GoogleRegisterView, GoogleLoginView, CARegisterAPIView

router = routers.DefaultRouter()
router.register(r'pre-register', PreRegistrationAPIView)
urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('register/google/', GoogleRegisterView.as_view(), name="google-register"),
    path('login/google/', GoogleLoginView.as_view(), name="google-login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('refresh/', CookieTokenRefreshView.as_view(), name="refresh"),
    path('user-details/', UserDetailAPI.as_view()),
    path('user-profile/', UserProfileAPIView.as_view(), name="create-user-profile"),
    path('user-profile-details/', UserProfileDetailsView.as_view(), name="user-details"),
    path('ca-register/', CARegisterAPIView.as_view(), name="ca-register"),
    path('', include(router.urls)),
]
