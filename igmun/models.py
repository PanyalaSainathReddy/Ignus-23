from django.db import models
from django.core.validators import RegexValidator

COMMITTEE_CHOICES = (
    ("DISEC", "Disarmament and International Security"),
    ("UNHRC", "United Nations Human Rights Council"),
    ("LS", "Lok Sabha"),
    ("UNODC", "United Nations Office on Drugs and Crime")
)


class EBForm(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    email = models.EmailField(unique=True)
    org = models.CharField(max_length=200)
    permanent_address = models.TextField()
    exp_eb = models.TextField(blank=True)
    exp_delegate = models.TextField(blank=True)
    preferred_comm = models.CharField(max_length=10, choices=COMMITTEE_CHOICES)

    class Meta:
        verbose_name = "EB Form"
        verbose_name_plural = "EB Forms"

    def __str__(self):
        return self.first_name + " " + self.last_name
