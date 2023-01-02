from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from registration.models import UserProfile


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

    name = models.CharField(max_length=2, choices=ETYPE_CHOICES, default='1')
    cover = models.ImageField(upload_to='event_type')
    about = RichTextUploadingField(blank=True)

    def __str__(self):
        return self.get_name_display()

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Event Types'


class Event(models.Model):
    name = models.CharField(max_length=32)
    slug = models.SlugField(blank=True, default="")
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True, blank=True, related_name="events", related_query_name="event")
    venue = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    cover = models.ImageField(upload_to='event', null=True, blank=True)
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    organizers = models.ManyToManyField(UserProfile)
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
                "name": organizer.user.get_full_name(),
                "email": organizer.user.email,
                "phone": organizer.phone
            }
            orgs.append(org)

        return orgs

    def get_absolute_url(self):
        return reverse("event", kwargs={"slug": self.slug})

    def save(self) -> None:
        self.slug = slugify(self.name)
        return super().save()
