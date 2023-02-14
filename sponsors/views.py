from rest_framework import permissions
from .models import Sponsors, SponsorDesignation
from .serializers import AllSponsorsSerializer
from rest_framework.generics import ListAPIView
from django.db.models import Prefetch


class AllSponsorsView(ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = AllSponsorsSerializer
    model = SponsorDesignation
    queryset = SponsorDesignation.objects.prefetch_related(
        Prefetch('sponsors', queryset=Sponsors.objects.filter(old_sponsor=False).order_by('sponsor_rank'), to_attr='new_sponsors')
    )
