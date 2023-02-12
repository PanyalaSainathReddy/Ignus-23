from django.contrib import admin
from import_export import fields, resources, widgets
from import_export.admin import ImportExportActionModelAdmin

from .models import Event, EventType, Location, Organizer, TeamRegistration


class EventInLine(admin.StackedInline):
    model = Event


class EventCategoryAdmin(admin.ModelAdmin):
    inlines = (EventInLine,)
    list_display = ['reference_name', 'type']

    class Meta:
        model = EventType


class EventResource(resources.ModelResource):
    userfield = fields.Field(
        column_name="registered_users",
        attribute="userprofile_set",
        widget=widgets.ManyToManyWidget("registration.UserProfile", field="registration_code", separator="; ")
    )

    class Meta:
        model = Event
        fields = ('name', 'userfield')


class EventAdmin(ImportExportActionModelAdmin):
    resource_class = EventResource
    list_display = ['name', 'get_event_type', 'number_registered', 'teams_registered', 'published']


class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'latitude', 'longitude', 'iframe']

    class Meta:
        model = Location


class OrganizerAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone']

    class Meta:
        model = Organizer


class TeamRegistrationAdmin(admin.ModelAdmin):
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
