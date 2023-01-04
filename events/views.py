from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer


class EventTypeView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventTypeSerializer
    model = EventType
    queryset = EventType.objects.all()


class EventView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = EventSerializer
    model = Event
    queryset = Event.objects.all()
    lookup_field = 'slug'
