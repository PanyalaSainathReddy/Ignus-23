from django.urls import path, include
from rest_framework import routers
from .views import SponsorListAPIViewSet

app_name = 'sponsors'

router = routers.DefaultRouter()
router.register(r'sponsors-list', SponsorListAPIViewSet, basename='sponsors-list')
urlpatterns = [
    path('', include(router.urls)),
]
