from django.contrib import admin

from .models import Event, EventType, Location, Organizer


class EventInLine(admin.StackedInline):
    model = Event


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (EventInLine,)
    list_display = ['type']

    class Meta:
        model = EventType


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'iframe']

    class Meta:
        model = Location


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

    class Meta:
        model = Organizer


admin.site.register(EventType, EventCategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organizer, OrganizerAdmin)
