from django.contrib import admin
from .models import EBForm


class EBFormAdmin(admin.ModelAdmin):
    list_display = ("__str__", "email", "org", "preferred_comm")


admin.site.register(EBForm, EBFormAdmin)
