from django.contrib import admin

from .models import Event, EventType, Location


class EventInLine(admin.StackedInline):
    model = Event


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (EventInLine,)
    list_display = ['name']

    class Meta:
        model = EventType


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'iframe']

    class Meta:
        model = Location


admin.site.register(EventType, EventCategoryAdmin)
admin.site.register(Location, LocationAdmin)
