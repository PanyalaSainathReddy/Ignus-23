from django.contrib import admin
from .models import EBForm, PreRegistrationForm


class EBFormAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm")


class PreRegistrationFormAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm")


admin.site.register(EBForm, EBFormAdmin)
admin.site.register(PreRegistrationForm, PreRegistrationFormAdmin)
