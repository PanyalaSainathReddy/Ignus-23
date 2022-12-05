from django.contrib import admin
from .models import EBForm, PreRegistrationForm
from import_export.admin import ExportActionMixin

class EBFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm1", "preferred_comm2", "preferred_comm3")


class PreRegistrationFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm")


admin.site.register(EBForm, EBFormAdmin)
admin.site.register(PreRegistrationForm, PreRegistrationFormAdmin)
