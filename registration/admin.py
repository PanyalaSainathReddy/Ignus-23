from django.contrib import admin

from .models import CampusAmbassador, PreRegistration, User, UserProfile


class UserAdmin(admin.ModelAdmin):
    class Meta:
        model = User


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'phone', 'gender', 'college', 'passes', 'amount_due', 'qr_code', 'registration_code', 'registration_code_igmun']
    list_filter = ['gender']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'user__email', 'college', 'phone']


class CampusAmbassadorAdmin(admin.ModelAdmin):
    list_display = ['ca_user', 'referral_code', 'number_referred']
    list_filter = ['ca_user__current_year']
    search_fields = ['referral_code', 'ca_user__user__first_name', 'ca_user__user__last_name', 'ca_user__phone']

    class Meta:
        model = CampusAmbassador


class PreRegistrationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'college')
    list_filter = ('college', 'current_year', 'college_state')

    class Meta:
        model = PreRegistration


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CampusAmbassador, CampusAmbassadorAdmin)
admin.site.register(PreRegistration, PreRegistrationAdmin)
