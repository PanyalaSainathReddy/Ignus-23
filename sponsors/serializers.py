from rest_framework import serializers
from .models import Sponsors


class SponsorSerializer(serializers.ModelSerializer):
    designation_sponsor_type = serializers.SerializerMethodField(read_only=True)
    designation_title_rank = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Sponsors
        fields = ['designation_sponsor_type', 'designation_title_rank', 'name', 'image', 'sponsor_link', 'old_sponsor', 'sponsor_rank']

    @staticmethod
    def get_designation_sponsor_type(obj):
        return obj.designation.sponsor_type

    @staticmethod
    def get_designation_title_rank(obj):
        return obj.designation.title_rank
