from rest_framework import serializers
from .models import TeamProfile


class TeamProfileSerializer(serializers.ModelSerializer):
    department_department_name = serializers.SerializerMethodField(read_only=True)
    department_department_rank = serializers.SerializerMethodField(read_only=True)
    department_published = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TeamProfile
        fields = ['department_department_name', 'department_department_rank', 'department_published', 'name', 'avatar', 'phone', 'insta_link', 'linkedin_link', 'twitter_link', 'github_link', 'team_member_rank', 'published']

    @staticmethod
    def get_department_department_name(obj):
        return obj.department.department_name

    @staticmethod
    def get_department_department_rank(obj):
        return obj.department.department_rank

    @staticmethod
    def get_department_published(obj):
        return obj.department.published
