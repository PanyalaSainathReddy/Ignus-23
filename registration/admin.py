from django.contrib import admin
from .models import UserProfile, TeamRegistration, PreRegistration


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'gender', 'college', 'id_issued', 'accommodation_required', 'qr_code']
    list_filter = ['gender', 'id_issued', 'accommodation_required']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'college', 'phone']


# class CampusAmbassadorAdmin(admin.ModelAdmin):
#     list_display = ['ca_user', 'referral_code', 'workshop_capability', 'number_referred']
#     list_filter = ['workshop_capability', 'ca_user__current_year']
#     search_fields = ['referral_code', 'ca_user__user__first_name', 'ca_user__user__last_name', 'ca_user__phone']

#     class Meta:
#         model = CampusAmbassador


class TeamRegistrationAdmin(admin.ModelAdmin):
    autocomplete_fields = ['leader', 'members']
    list_display = ['__str__', 'event', 'leader']
    list_filter = ['event']
    search_fields = ['leader__user__first_name', 'leader__user__last_name', 'leader__user__email', 'leader__phone']

    class Meta:
        model = TeamRegistration


class PreRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'college')
    list_filter = ('college', 'gender', 'current_year', 'college_state')

    class Meta:
        model = PreRegistration


admin.site.register(UserProfile, UserProfileAdmin)
# admin.site.register(CampusAmbassador, CampusAmbassadorAdmin)
admin.site.register(TeamRegistration, TeamRegistrationAdmin)
admin.site.register(PreRegistration, PreRegistrationAdmin)
