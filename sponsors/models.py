from django.db import models


class SponsorDesignation(models.Model):
    sponsor_type = models.CharField(max_length=150, verbose_name='Sponsor Type')
    title_rank = models.IntegerField(default=1, verbose_name='Hierarchial position of the title')

    def __str__(self):
        return self.sponsor_type


class Sponsors(models.Model):
    designation = models.ForeignKey(SponsorDesignation, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='sponsors/', verbose_name='sponsors Logo')
    name = models.CharField(default='', max_length=150, verbose_name='Sponsor name', blank=True)
    sponsor_link = models.URLField(default='', max_length=1500, verbose_name='Link to Sponsors website', blank=True)
    sponsor_rank = models.IntegerField(default=1, verbose_name='Relative position of the sponsor')
    old_sponsor = models.BooleanField(default=False, verbose_name='Is this an old sponsor?')

    class Meta:
        verbose_name_plural = 'sponsors'

    def __str__(self):
        return self.name
