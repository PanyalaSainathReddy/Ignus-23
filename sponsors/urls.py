from django.urls import path
from .views import AllSponsorsView

app_name = 'sponsors'

urlpatterns = [
    path('list/', AllSponsorsView.as_view(), name="sponsors"),
]
