from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
# import serializers

from .models import Event, EventType
from .serializers import AllEventsSerializer, EventTypeSerializer


# class EventView(ListAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = EventSerializer
#     model = Event
#     queryset = Event.objects.filter(published=True)
#     lookup_field = 'slug'


class AllEventsView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AllEventsSerializer
    model = EventType
    queryset = EventType.objects.prefetch_related(
        Prefetch('events', queryset=Event.objects.filter(published=True), to_attr='published_events')
    )


class EventTypeView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventTypeSerializer
    model = EventType

    def get(self, request, reference_name):
        queryset = EventType.objects.get(reference_name=reference_name)

        serializer = EventTypeSerializer(queryset)
        return Response(serializer.data)
