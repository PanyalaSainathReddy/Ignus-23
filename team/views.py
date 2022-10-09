from rest_framework import viewsets
from rest_framework import permissions
from .models import TeamProfile
from .serializers import TeamProfileSerializer


class TeamProfileAPIViewSet(viewsets.ModelViewSet):
    serializer_class = TeamProfileSerializer
    permission_classes = [permissions.AllowAny]
    ordering_fields = ['department_department_rank']

    def get_queryset(self):
        return TeamProfile.objects.all()
