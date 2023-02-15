from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from import_export import resources
from import_export.admin import ExportActionMixin, ImportExportActionModelAdmin

from .models import CampusAmbassador, PreCA, PreRegistration, UserProfile, BlacklistedEmail

User = get_user_model()


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('profile_complete', 'iitj')}),
        ('Google', {'fields': ('is_google', 'google_picture')})
    )

    list_display = UserAdmin.list_display + ('is_google', 'profile_complete', 'iitj')
    list_filter = UserAdmin.list_filter + ('profile_complete', 'is_google', 'iitj')

    class Meta:
        model = User


class BlacklistedEmailAdmin(admin.ModelAdmin):
    class Meta:
        model = BlacklistedEmail


class PreCAAdmin(admin.ModelAdmin):
    list_display = ["__str__", "email", "phone_number", "college", "college_state", "current_year"]
    list_filter = ['current_year', 'college_state']
    search_fields = ['__str__', 'college', 'college_state', 'phone_number']

    class Meta:
        model = PreCA


class UserProfileResource(resources.ModelResource):
    class Meta:
        model = UserProfile
        fields = ('user__first_name', 'user__last_name', 'user__email', 'phone', 'college', 'gender', 'registration_code', 'amount_paid', 'accomodation_4', 'accomodation_2', 'flagship', 'igmun', 'igmun_pref', 'mun_exp')


class UserProfileAdmin(ImportExportActionModelAdmin):
    resource_class = UserProfileResource
    list_display = ['__str__', 'registration_code', 'phone', 'gender', 'college', 'qr_code', 'pronites_qr']
    list_filter = ['gender', 'igmun', 'flagship', 'amount_paid', 'accomodation_4', 'accomodation_2', 'is_ca']
    search_fields = ['user__username', 'registration_code', 'user__first_name', 'user__last_name', 'user__email', 'college', 'phone']


class CampusAmbassadorAdmin(admin.ModelAdmin):
    list_display = ['ca_user', 'referral_code', 'number_referred']
    list_filter = ['ca_user__current_year']
    search_fields = ['referral_code', 'ca_user__user__first_name', 'ca_user__user__last_name', 'ca_user__phone']

    class Meta:
        model = CampusAmbassador


class PreRegistrationAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'college', 'current_year', 'college_state')
    list_filter = ('college', 'current_year', 'college_state')

    class Meta:
        model = PreRegistration


admin.site.register(User, CustomUserAdmin)
admin.site.register(BlacklistedEmail, BlacklistedEmailAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(CampusAmbassador, CampusAmbassadorAdmin)
admin.site.register(PreRegistration, PreRegistrationAdmin)
admin.site.register(PreCA, PreCAAdmin)
