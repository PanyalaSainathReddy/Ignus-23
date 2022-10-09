from rest_framework import viewsets
from rest_framework import permissions
from .models import Sponsors
from .serializers import SponsorSerializer


class SponsorListAPIViewSet(viewsets.ModelViewSet):
    serializer_class = SponsorSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['designation_title_rank']

    def get_queryset(self):
        return Sponsors.objects.all()
