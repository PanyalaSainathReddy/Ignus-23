import uuid
# import re
from django.db import models
from django.db.models import Count
# from django.db.models.signals import pre_save
# from django.db.models.signals import post_save
# from django.db.models import Sum, Q
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.shortcuts import reverse
from django.utils.safestring import mark_safe
from events.models import Event
# from workshops.models import Workshop
# from .utils import unique_ca_referral_code


class PreRegistration(models.Model):
    # choices
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Other'),
    )
    YEAR_CHOICES = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('5', 'Fifth Year'),
        ('6', 'Other')
    )
    STATE_CHOICES = (
        ('1', 'Andhra Pradesh'),
        ('2', 'Arunachal Pradesh'),
        ('3', 'Assam'),
        ('4', 'Bihar'),
        ('5', 'Chhattisgarh'),
        ('6', 'Goa'),
        ('7', 'Gujarat'),
        ('8', 'Haryana'),
        ('9', 'Himachal Pradesh'),
        ('10', 'Jammu & Kashmir'),
        ('11', 'Jharkhand'),
        ('12', 'Karnataka'),
        ('13', 'Kerala'),
        ('14', 'Madhya Pradesh'),
        ('15', 'Maharashtra'),
        ('16', 'Manipur'),
        ('17', 'Meghalaya'),
        ('18', 'Mizoram'),
        ('19', 'Nagaland'),
        ('20', 'Odisha'),
        ('21', 'Punjab'),
        ('22', 'Rajasthan'),
        ('23', 'Sikkim'),
        ('24', 'Tamil Nadu'),
        ('25', 'Telangana'),
        ('26', 'Tripura'),
        ('27', 'Uttarakhand'),
        ('28', 'Uttar Pradesh'),
        ('29', 'West Bengal'),
        ('30', 'Andaman & Nicobar Islands'),
        ('31', 'Delhi'),
        ('32', 'Chandigarh'),
        ('33', 'Dadra & Naagar Haveli'),
        ('34', 'Daman & Diu'),
        ('35', 'Lakshadweep'),
        ('36', 'Puducherry'),
    )
    # Validators
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    # Model
    full_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    college = models.CharField(max_length=100)
    college_state = models.CharField(max_length=2, choices=STATE_CHOICES, default='22')
    current_year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    por = models.CharField(max_length=500, blank=True, default='')
    por_holder_contact = models.CharField(max_length=1000, blank=True, default='')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Pre Registration'
        verbose_name_plural = 'Pre Registrations'


class UserProfile(models.Model):
    # choices
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('T', 'Other'),
    )
    YEAR_CHOICES = (
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
        ('5', 'Fifth Year'),
        ('6', 'Other')
    )
    STATE_CHOICES = (
        ('1', 'Andhra Pradesh'),
        ('2', 'Arunachal Pradesh'),
        ('3', 'Assam'),
        ('4', 'Bihar'),
        ('5', 'Chhattisgarh'),
        ('6', 'Goa'),
        ('7', 'Gujarat'),
        ('8', 'Haryana'),
        ('9', 'Himachal Pradesh'),
        ('10', 'Jammu & Kashmir'),
        ('11', 'Jharkhand'),
        ('12', 'Karnataka'),
        ('13', 'Kerala'),
        ('14', 'Madhya Pradesh'),
        ('15', 'Maharashtra'),
        ('16', 'Manipur'),
        ('17', 'Meghalaya'),
        ('18', 'Mizoram'),
        ('19', 'Nagaland'),
        ('20', 'Odisha'),
        ('21', 'Punjab'),
        ('22', 'Rajasthan'),
        ('23', 'Sikkim'),
        ('24', 'Tamil Nadu'),
        ('25', 'Telangana'),
        ('26', 'Tripura'),
        ('27', 'Uttarakhand'),
        ('28', 'Uttar Pradesh'),
        ('29', 'West Bengal'),
        ('30', 'Andaman & Nicobar Islands'),
        ('31', 'Delhi'),
        ('32', 'Chandigarh'),
        ('33', 'Dadra & Naagar Haveli'),
        ('34', 'Daman & Diu'),
        ('35', 'Lakshadweep'),
        ('36', 'Puducherry'),
    )
    # Validators
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    # Model
    # referred_by = models.ForeignKey('CampusAmbassador', blank=True, null=True, on_delete=models.SET_NULL)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=10, validators=[contact])
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='M')
    current_year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')
    college = models.CharField(max_length=128)
    address = models.CharField(max_length=128)
    state = models.CharField(max_length=2, choices=STATE_CHOICES)
    id_issued = models.BooleanField(default=False)
    accommodation_required = models.BooleanField(default=False)
    # registration_paid = models.BooleanField(default=False)
    # accommodation_paid = models.BooleanField(default=False)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, unique=True)
    # events_registered = models.ManyToManyField(Event, limit_choices_to={'max_team_size': 1}, blank=True)
    # workshops_registered = models.ManyToManyField(Workshop, through='WorkshopRegistration',
    #                                             through_fields=('userprofile', 'workshop'), blank=True)

    class Meta:
        ordering = ['user__first_name']

    # objects = UserProfileManager()

    def __str__(self):
        return '{ig_number} ({name})'.format(ig_number=self.user.username, name=self.user.get_full_name())

    @property
    def team_events_registered(self):
        return Event.objects.filter(id__in=self.team_registrations().values_list('event', flat=True))

    def team_registrations(self):
        result = self.teamregistration_set.all() | self.team_leader.all()
        return result.distinct()

    def get_absolute_url(self):
        return reverse('accounts:user-detail', kwargs={'ignumber': self.user.username})

    # @property
    # def amount_paid(self):
    #     amount = self.transactiondetail_set.aggregate(amount_paid=Sum('amount'))['amount_paid']
    #     return 0 if amount is None else amount

    def get_event_string(self):
        return 'Events-{uuidhalf}'.format(uuidhalf=str(self.uuid)[:13])

    def get_accommodation_string(self):
        return 'Accommodation-{ig_no}-{uuidhalf}'.format(uuidhalf=str(self.uuid)[-12:], ig_no=self.user.username)

    def get_igmun_string(self):
        return 'Igmun-{uuidhalf}'.format(uuidhalf=str(self.uuid)[:13])

    # @property
    # def accommodation_done(self):
    #     transaction = self.transactiondetail_set.filter(description__contains=self.get_accommodation_string(),
    #                                                     transaction__confirmed=True).first()
    #     return True if transaction else False

    # def get_invoice_data(self):
    #     data = {}
    #     workshop_list = []
    #     workshop_registration_list = self.workshopregistration_set.all()
    #     for workshop_registration in workshop_registration_list:
    #         if not workshop_registration.get_payment_status():
    #             workshop_list.append(workshop_registration.get_workshop_string())
    #     data['workshops'] = workshop_list
    #     if not self.registration_amount_paid:
    #         data['reg_cum_event_fee'] = self.get_event_string()
    #     if not self.accommodation_done:
    #         data['accommodation_fee'] = self.get_accommodation_string()
    #     if not self.igmunregistration.paid:
    #         data['igmun_fee'] = self.get_igmun_string()
    #     return data

    def qr_code(self):
        return mark_safe('<img src="https://chart.apis.google.com/chart?chs=150x150&cht=qr&chl={data}&choe=UTF-8" \
                style="width: 120px; height: 120px" />'.format(data=self.uuid))

    qr_code.short_description = 'qr code'
    qr_code.allow_tags = True

    # @property
    # def registration_amount_paid(self):
    #     approved = False
    #     transaction = self.transactiondetail_set.filter(description__contains=self.get_event_string(),
    #                                                     transaction__confirmed=True)
    #     igmun_paid = self.igmunregistration.paid
    #     workshop_paid = False
    #     for workshop in self.workshopregistration_set.all():
    #         if workshop.get_payment_status():
    #             workshop_paid = True
    #     if transaction or igmun_paid or workshop_paid:
    #         approved = True
    #     return True if approved else False


# class CampusAmbassador(models.Model):
#     ca_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='ca_user')
#     insta_link = models.URLField()
#     workshop_capability = models.BooleanField(default=False)
#     publicize_ignus = models.TextField(max_length=512)
#     past_experience = models.TextField(max_length=512)
#     description = models.TextField(max_length=512, blank=True, default='')
#     timestamp = models.DateTimeField(auto_now_add=True)
#     referral_code = models.CharField(max_length=7, editable=False, unique=True, primary_key=True)

#     class Meta:
#         ordering = ['-timestamp']

#     @property
#     def number_referred(self):
#         return self.userprofile_set.count()

#     def __str__(self):
#         return "{name} ({code})".format(name=self.ca_user.user.first_name, code=self.referral_code)


# def pre_save_campus_ambassador(sender, instance, **kwargs):
#     if instance._state.adding is True:
#         instance.referral_code = unique_ca_referral_code(instance)


# def post_save_campus_ambassador(sender, instance, created, **kwargs):
#     if created:
#         send_ca_confirmation_mail(instance=instance)


# pre_save.connect(pre_save_campus_ambassador, sender=CampusAmbassador)

# post_save.connect(post_save_campus_ambassador, sender=CampusAmbassador)


class TeamRegistrationManager(models.Manager):
    def user_profiles_count(self):
        return self.aggregate(members_count=Count('members'))['members_count'] + \
               self.aggregate(leader_count=Count('leader'))['leader_count']


class TeamRegistration(models.Model):
    leader = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='team_leader')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, limit_choices_to={'max_team_size__gt': 1})
    members = models.ManyToManyField(UserProfile, blank=True)

    objects = TeamRegistrationManager()

    def __str__(self):
        return "{event} - {leader}".format(leader=self.leader, event=self.event)
