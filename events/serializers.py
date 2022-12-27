from rest_framework import serializers

from .models import Event, EventType


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ("name", "slug", "event_type", "venue", "start_time", "end_time", "cover", "pdf", "get_organizers", "team_event", "max_team_size", "min_team_size", "about", "details", "google_form", "custom_html", "published")
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class EventTypeSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = EventType
        fields = ("name", "cover", "about", "events")
