from django.contrib import admin

from .models import Event, EventType, Location, Organizer, TeamRegistration


class EventInLine(admin.StackedInline):
    model = Event


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (EventInLine,)
    list_display = ['reference_name', 'type']

    class Meta:
        model = EventType


class EventAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_event_type', 'number_registered', 'published']

    class Meta:
        model = Event


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'iframe']

    class Meta:
        model = Location


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

    class Meta:
        model = Organizer


class TeamRegistrationAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['leader', 'members']
    list_display = ['id', 'event', 'leader', 'number_of_members']
    list_filter = ['event']
    search_fields = ['leader__user__first_name', 'leader__user__last_name', 'leader__user__email', 'leader__phone']

    class Meta:
        model = TeamRegistration


admin.site.register(EventType, EventCategoryAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(TeamRegistration, TeamRegistrationAdmin)
