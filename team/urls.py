from django.urls import path, include
from rest_framework import routers
from .views import TeamProfileAPIViewSet

app_name = 'team'

router = routers.DefaultRouter()
router.register(r'team-profiles-list', TeamProfileAPIViewSet, basename='team-profiles-list')
urlpatterns = [
    path('', include(router.urls)),
]
