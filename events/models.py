from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator
from django.db import models
from django.db.models.signals import pre_save
from django.utils.safestring import mark_safe

from registration.models import UserProfile


class Organizer(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=128)
    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    def __str__(self):
        return self.name

    @property
    def iframe(self):
        return mark_safe(
            '<iframe width="200" height="200" style="border: none"'
            'src="https://maps.google.com/maps?q={lat},{long}&hl=es;z=14&amp;output=embed"></iframe>'.format(
                lat=self.latitude, long=self.longitude))


class EventType(models.Model):
    ETYPE_CHOICES = (
        ('1', 'Cultural Event'),
        ('2', 'Informal Event'),
        ('3', 'Pronites'),
        ('4', 'Flagship Event'),
        ('5', 'Online Event')
    )

    type = models.CharField(max_length=2, choices=ETYPE_CHOICES, default='1')
    reference_name = models.CharField(max_length=20, unique=False, default="")
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    organizers = models.ManyToManyField(Organizer)

    def __str__(self):
        return self.reference_name

    class Meta:
        ordering = ['type']
        verbose_name_plural = 'Event Types'

    def name(self):
        return self.get_type_display()

    def get_organizers(self):
        orgs = []
        for organizer in self.organizers.all():
            org = {
                "name": organizer.name,
                "email": organizer.email,
                "phone": organizer.phone
            }
            orgs.append(org)

        return orgs


class Event(models.Model):
    name = models.CharField(max_length=32)
    # slug = models.SlugField(blank=True, default="")
    sub_title = models.CharField(max_length=64, blank=True, default="")
    team_id_code = models.CharField(max_length=5, blank=True)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True, blank=True, related_name="events", related_query_name="event")
    venue = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(upload_to='event', null=True, blank=True)
    team_event = models.BooleanField(default=False)
    max_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    min_team_size = models.PositiveSmallIntegerField(default=1, help_text='Select minimum number of participants for event.')
    about = RichTextUploadingField(blank=True)
    rank = models.PositiveSmallIntegerField(default=0, help_text='Rank of event in event type')
    gform_link = models.URLField(blank=True, default="")
    ol_live = models.BooleanField(default=False)
    # details = RichTextUploadingField(blank=True, default="")
    # results = models.TextField(blank=True, default="")
    # google_form = models.URLField(blank=True)
    # custom_html = models.TextField(blank=True, default="")
    published = models.BooleanField(default=True)

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.name

    def get_event_type(self):
        return self.event_type.name()

    def get_venue(self):
        if self.venue is not None:
            venue = {
                "name": self.venue.name,
                "lat": self.venue.latitude,
                "long": self.venue.longitude,
                "iframe": self.venue.iframe
            }

            return venue

    def number_registered(self):
        return self.userprofile_set.count()

    # def get_absolute_url(self):
    #     return reverse("event", kwargs={"slug": self.slug})

    # def save(self) -> None:
    #     self.slug = slugify(self.reference_name)
    #     return super().save()


class TeamRegistration(models.Model):
    id = models.CharField(max_length=20, unique=True, primary_key=True, editable=False)
    leader = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    members = models.ManyToManyField(UserProfile, related_name="teams", related_query_name="team", blank=True)
    event = models.ForeignKey(Event, on_delete=models.DO_NOTHING, related_name="teams", related_query_name="team")

    def __str__(self):
        return self.id

    class Meta:
        verbose_name_plural = "Team Registrations"

    def number_of_members(self):
        return self.members.count()

    def member_list(self):
        members = []

        for member in self.members.all():
            mem = {
                "id": member.registration_code,
                "name": member.user.get_full_name()
            }

            members.append(mem)

        return members


def pre_save_team_registration(sender, instance, **kwargs):
    if instance._state.adding is True:
        instance.id = instance.leader.registration_code + "-" + instance.event.team_id_code


pre_save.connect(pre_save_team_registration, sender=TeamRegistration)
