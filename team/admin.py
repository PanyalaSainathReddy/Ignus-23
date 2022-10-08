from django.contrib import admin
from .models import Departments, TeamProfile


class TeamProfileAdmin(admin.ModelAdmin):
    model = TeamProfile
    list_display = ['name', 'department', 'phone', 'published']
    list_filter = ['department', 'published']
    search_fields = ['name', 'phone']
    ordering = ['team_member_rank']


class DepartmentsAdmin(admin.ModelAdmin):
    model = Departments
    list_display = ['department_name', 'published']
    list_filter = ['published']
    ordering = ['department_rank']

    class Meta:
        model = Departments
        fields = '__all__'


admin.site.register(TeamProfile, TeamProfileAdmin)
admin.site.register(Departments, DepartmentsAdmin)
