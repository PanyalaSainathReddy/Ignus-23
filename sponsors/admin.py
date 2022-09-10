from django.contrib import admin
from .models import SponsorDesignation, Sponsors


class SponsorsAdmin(admin.StackedInline):
    model = Sponsors
    ordering = ['sponsor_rank']


class SponsorsDesignationAdmin(admin.ModelAdmin):
    model = SponsorDesignation
    list_display = ['sponsor_type']
    inlines = [SponsorsAdmin, ]
    ordering = ['title_rank']

    class Meta:
        model = Sponsors
        fields = '__all__'


admin.site.register(SponsorDesignation, SponsorsDesignationAdmin)
