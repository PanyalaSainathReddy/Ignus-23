from django.db.models import Prefetch
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer


class EventTypeView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventTypeSerializer
    model = EventType
    queryset = EventType.objects.prefetch_related(
        Prefetch('events', queryset=Event.objects.filter(published=True), to_attr='published_events')
    )


class EventView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    model = Event
    queryset = Event.objects.filter(published=True)
    lookup_field = 'slug'
