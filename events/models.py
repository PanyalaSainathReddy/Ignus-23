from ckeditor_uploader.fields import RichTextUploadingField
from django.core.validators import RegexValidator
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify


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
        ('2', 'Flagship Event'),
        ('3', 'Technical Event'),
        ('4', 'Prakriti'),
        ('5', 'Informals Event')
    )

    type = models.CharField(max_length=2, choices=ETYPE_CHOICES, default='1')
    cover = models.ImageField(upload_to='event_type')
    about = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.get_type_display()

    class Meta:
        ordering = ['type']
        verbose_name_plural = 'Event Types'

    def name(self):
        return self.get_type_display()


class Event(models.Model):
    name = models.CharField(max_length=32)
    reference_name = models.CharField(max_length=20, unique=False, default="")
    slug = models.SlugField(blank=True, default="")
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True, blank=True, related_name="events", related_query_name="event")
    venue = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(upload_to='event', null=True, blank=True)
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    organizers = models.ManyToManyField(Organizer)
    team_event = models.BooleanField(default=False)
    max_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    min_team_size = models.PositiveSmallIntegerField(default=1, help_text='Select minimum number of participants for event.')
    about = RichTextUploadingField(blank=True)
    details = RichTextUploadingField(blank=True, default="")
    results = models.TextField(blank=True, default="")
    google_form = models.URLField(blank=True)
    custom_html = models.TextField(blank=True, default="")
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

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

    def get_absolute_url(self):
        return reverse("event", kwargs={"slug": self.slug})

    def save(self) -> None:
        self.slug = slugify(self.reference_name)
        return super().save()
