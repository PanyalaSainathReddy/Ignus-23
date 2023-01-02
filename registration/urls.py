from django.urls import path, include
from rest_framework import routers
from .views import UserDetailAPI, RegisterUserAPIView, UserProfileAPIView, UserProfileDetailsView, PreRegistrationAPIView, LoginView, LogoutView, CookieTokenRefreshView, PreCARegistrationAPIView

router = routers.DefaultRouter()
router.register(r'pre-register', PreRegistrationAPIView)
router.register(r'ca-register-pre', PreCARegistrationAPIView)
urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('refresh/', CookieTokenRefreshView.as_view(), name="refresh"),
    path('user-details/', UserDetailAPI.as_view()),
    path('user-profile/', UserProfileAPIView.as_view()),
    path('user-profile-details/', UserProfileDetailsView.as_view()),
    # path('ca-register/', CARegisterAPIView.as_view()),
    # path('ca-register-pre/', PreCARegistrationAPIView.as_view()),
    path('', include(router.urls)),
]
