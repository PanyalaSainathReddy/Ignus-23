from django.contrib import admin
from .models import EBForm, PreRegistrationForm, PreCA
from import_export.admin import ExportActionMixin


class PreCAAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "phone_number", "college", "college_state", "current_year")


class EBFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm1", "preferred_comm2", "preferred_comm3")


class PreRegistrationFormAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm1", "preferred_comm2", "preferred_comm3")


admin.site.register(EBForm, EBFormAdmin)
admin.site.register(PreRegistrationForm, PreRegistrationFormAdmin)
admin.site.register(PreCA, PreCAAdmin)
