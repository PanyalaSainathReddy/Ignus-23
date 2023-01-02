from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import EBForm, IGMUNCampusAmbassador, PreRegistrationForm


class EBFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm1", "preferred_comm2", "preferred_comm3")


class PreRegistrationFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm1", "preferred_comm2", "preferred_comm3")


class IGMUNCampusAmbassadorAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['ca_user', 'referral_code', 'number_referred']
    search_fields = ['referral_code', 'ca_user__user__first_name', 'ca_user__user__last_name', 'ca_user__phone']

    class Meta:
        model = IGMUNCampusAmbassador


admin.site.register(EBForm, EBFormAdmin)
admin.site.register(PreRegistrationForm, PreRegistrationFormAdmin)
admin.site.register(IGMUNCampusAmbassador, IGMUNCampusAmbassadorAdmin)
