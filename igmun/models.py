from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save

from registration.models import UserProfile


class PreCA(models.Model):
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
    city = models.CharField(max_length=50)
    college = models.CharField(max_length=100)
    college_state = models.CharField(max_length=2, choices=STATE_CHOICES, default='22')
    current_year = models.CharField(max_length=1, choices=YEAR_CHOICES, default='1')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'CA Pre Registration'
        verbose_name_plural = 'CA Pre Registrations'


COMMITTEE_CHOICES = (
    ("DISEC", "Disarmament and International Security"),
    ("UNHRC", "United Nations Human Rights Council"),
    ("ESS-UNGA", "Emergency Special Session United Nations General Assembly"),
    ("LS", "Lok Sabha")
)


class EBForm(models.Model):
    full_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(unique=True)
    org = models.CharField(max_length=200)
    city = models.TextField()
    exp_eb = models.TextField(blank=True, default="")
    exp_delegate = models.TextField(blank=True, default="")
    preferred_comm1 = models.CharField(max_length=10, choices=COMMITTEE_CHOICES, default="")
    preferred_comm2 = models.CharField(max_length=10, choices=COMMITTEE_CHOICES, default="")
    preferred_comm3 = models.CharField(max_length=10, choices=COMMITTEE_CHOICES, default="")

    class Meta:
        verbose_name = "EB Form"
        verbose_name_plural = "EB Forms"

    def __str__(self):
        return self.full_name


class PreRegistrationForm(models.Model):
    full_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(unique=True)
    org = models.CharField(max_length=200)
    city = models.TextField()
    exp_delegate = models.TextField(blank=True, default="")
    preferred_comm1 = models.CharField(max_length=10, choices=COMMITTEE_CHOICES, default="")
    preferred_comm2 = models.CharField(max_length=10, choices=COMMITTEE_CHOICES, default="")
    preferred_comm3 = models.CharField(max_length=10, choices=COMMITTEE_CHOICES, default="")

    class Meta:
        verbose_name = "Pre Registration Form"
        verbose_name_plural = "Pre Registration Forms"

    def __str__(self):
        return self.full_name


class IGMUNCampusAmbassador(models.Model):
    ca_user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    referral_code = models.CharField(max_length=15, editable=False, unique=True, primary_key=True)
    verified = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "IGMUN Campus Ambassadors"

    @property
    def number_referred(self):
        return self.referred_igmun_users.count()

    def __str__(self):
        return self.ca_user.user.get_full_name()


def pre_save_campus_ambassador(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.referral_code = instance.ca_user.registration_code_igmun


pre_save.connect(pre_save_campus_ambassador, sender=IGMUNCampusAmbassador)
