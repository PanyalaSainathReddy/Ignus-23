from django.db import models
# from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import RichTextUploadingField


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
    # ETYPE_CHOICES = (
    #     ('1', 'Cultural Event'),
    #     ('2', 'Flagship Event'),
    #     ('3', 'Technical Event'),
    #     ('4', 'Prakriti'),
    #     ('5', 'Informals Event')

    # )
    name = models.CharField(max_length=128)
    # parent_type = models.CharField(max_length=1, choices=ETYPE_CHOICES, verbose_name='event type')
    cover = models.ImageField(upload_to='event_type')
    slug = models.SlugField()
    about = RichTextUploadingField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Event Types'


class Event(models.Model):
    name = models.CharField(max_length=32)
    # sub_name = models.CharField(max_length=32, blank=True)
    slug = models.SlugField()
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, null=True, blank=True)
    venue = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    unique_id = models.CharField(max_length=8)
    cover = models.ImageField(upload_to='event', null=True, blank=True)
    pdf = models.FileField(upload_to='pdf', null=True, blank=True)
    # organisers = models.ManyToManyField(AdminProfile)
    max_team_size = models.PositiveSmallIntegerField(default=1, help_text='Leave 1 for single participant event')
    min_team_size = models.PositiveSmallIntegerField(default=1, help_text='Select minimum number of participants for event.')
    about = RichTextUploadingField()
    # about_plain = models.TextField(blank=True)
    details = RichTextUploadingField(null=True, blank=True, default='')
    # details_plain = models.TextField(blank=True)
    results = models.TextField(blank=True)
    # google_form = models.URLField(blank=True)
    custom_html = models.TextField(blank=True, default='')
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse_lazy('events:event-category', kwargs={'slug': self.event_type.slug})

    # def get_register_api_url(self):
    #     return reverse_lazy('api:events:register', kwargs={'unique_id': self.unique_id})

    # def get_admin_portal_url(self):
    #     return reverse_lazy('adminportal:event-detail', kwargs={
    #         'event_type': self.event_type.parent_type,
    #         'slug': self.slug
    #     })

    # def get_csv_download_url(self):
    #     return reverse_lazy('adminportal:event-registration-download', kwargs={
    #         'event_type': self.event_type.parent_type,
    #         'slug': self.slug
    #     })

    # def get_fa_icon(self):
    #     """Simple hack to get font awesome icon for an event object"""
    #     _map = {
    #         '1': 'fa-music',
    #         '2': 'fa-bolt',
    #         '3': 'fa-code',
    #         '4': 'fa-globe',
    #     }
    #     return _map.get(self.event_type.parent_type, 'fa-question')
