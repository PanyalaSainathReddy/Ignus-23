from rest_framework import serializers
from .models import Sponsors, SponsorDesignation


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsors
        fields = ['name', 'image', 'sponsor_link', 'old_sponsor', 'sponsor_rank']


class AllSponsorsSerializer(serializers.ModelSerializer):
    sponsors = SponsorSerializer(source="new_sponsors", many=True, read_only=True)

    class Meta:
        model = SponsorDesignation
        fields = ("sponsor_type", "title_rank", "sponsors")
