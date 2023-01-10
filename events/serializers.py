from rest_framework import serializers

from .models import Event, EventType


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            "name", "get_event_type", "get_venue", "start_time", "end_time",
            "cover", "team_event", "max_team_size", "min_team_size", "about",
            "rank", "published"
        )
        # extra_kwargs = {
        #     'url': {'lookup_field': 'slug'}
        # }


class AllEventsSerializer(serializers.ModelSerializer):
    events = EventSerializer(source="published_events", many=True, read_only=True)

    class Meta:
        model = EventType
        fields = ("reference_name", "name", "pdf", "get_organizers", "events")


class EventTypeSerializer(serializers.ModelSerializer):
    events = EventSerializer(many=True, read_only=True)

    class Meta:
        model = EventType
        fields = ("reference_name", "name", "pdf", "get_organizers", "events")
