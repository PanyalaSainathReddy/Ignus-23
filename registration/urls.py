from django.urls import path, include
from rest_framework import routers
from .views import UserDetailAPI, RegisterUserAPIView, UserProfileAPIView, UserProfileDetailsView, PreRegistrationAPIView, LoginView, LogoutView, CookieTokenRefreshView, PreCARegistrationAPIView, RegisterTeamAPIView, ImageUpload, AddTeamMembersAPIView, DeleteTeamAPIView, TeamDetailsAPIView

router = routers.DefaultRouter()
router.register(r'pre-register', PreRegistrationAPIView)
router.register(r'ca-pre-register', PreCARegistrationAPIView)
urlpatterns = [
    path('register/', RegisterUserAPIView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('refresh/', CookieTokenRefreshView.as_view(), name="refresh"),
    path('user-details/', UserDetailAPI.as_view()),
    path('user-profile/', UserProfileAPIView.as_view()),
    path('user-profile-details/', UserProfileDetailsView.as_view()),
    # path('ca-register/', CARegisterAPIView.as_view()),
    # path('ca-pre-register/', PreCARegistrationAPIView.as_view()),
    path('register-team/', RegisterTeamAPIView.as_view()),
    path('update-team/', AddTeamMembersAPIView.as_view()),
    path('team-details/', TeamDetailsAPIView.as_view()),
    path('delete-team/', DeleteTeamAPIView.as_view()),
    path('avatar-upload/', ImageUpload.as_view()),
    path('', include(router.urls)),
]
