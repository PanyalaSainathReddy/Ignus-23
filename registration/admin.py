from django.contrib import admin
from .models import UserProfile, PreRegistration, CampusAmbassador, PreCA, TeamRegistration


class PreCAAdmin(admin.ModelAdmin):
    list_display = ["__str__", "email", "phone_number", "college", "college_state", "current_year"]
    list_filter = ['current_year', 'college_state']
    search_fields = ['__str__', 'college', 'college_state', 'phone_number']

    class Meta:
        model = PreCA


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'gender', 'college', 'id_issued', 'accommodation_required', 'qr_code', 'registration_code']
    list_filter = ['gender', 'id_issued', 'accommodation_required']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'college', 'phone']


class CampusAmbassadorAdmin(admin.ModelAdmin):
    list_display = ['ca_user', 'referral_code', 'number_referred']
    list_filter = ['ca_user__current_year']
    search_fields = ['referral_code', 'ca_user__user__first_name', 'ca_user__user__last_name', 'ca_user__phone']

    class Meta:
        model = CampusAmbassador


class TeamRegistrationAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['leader', 'members']
    list_display = ['id', 'event', 'leader', 'number_of_members']
    list_filter = ['event']
    search_fields = ['leader__user__first_name', 'leader__user__last_name', 'leader__user__email', 'leader__phone']

    class Meta:
        model = TeamRegistration


class PreRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'college', 'current_year', 'college_state')
    list_filter = ('college', 'current_year', 'college_state')

    class Meta:
        model = PreRegistration


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CampusAmbassador, CampusAmbassadorAdmin)
admin.site.register(TeamRegistration, TeamRegistrationAdmin)
admin.site.register(PreRegistration, PreRegistrationAdmin)
admin.site.register(PreCA, PreCAAdmin)
