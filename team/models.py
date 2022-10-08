from django.db import models
from django.core.validators import RegexValidator


class Departments(models.Model):
    department_name = models.CharField(max_length=150, verbose_name='Department Name')
    department_rank = models.IntegerField(default=1, verbose_name='Hierarchial position of the department')
    published = models.BooleanField(default=True, verbose_name='Published')

    class Meta:
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.department_name


class TeamProfile(models.Model):
    # validators
    contact = RegexValidator(r'^[0-9]{10}$', message='Not a valid number!')
    # model
    name = models.CharField(default='', max_length=150, verbose_name='Name', blank=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='core_team/', verbose_name='avatar')
    phone = models.CharField(max_length=10, validators=[contact])
    insta_link = models.URLField(default='', max_length=1500, verbose_name='Instagram Link', blank=True)
    linkedin_link = models.URLField(default='', max_length=1500, verbose_name='LinkedIn Link', blank=True)
    twitter_link = models.URLField(default='', max_length=1500, verbose_name='Twitter Link', blank=True)
    github_link = models.URLField(default='', max_length=1500, verbose_name='Github Link', blank=True)
    team_member_rank = models.IntegerField(default=1, verbose_name='Relative position of the team member')
    published = models.BooleanField(default=True, verbose_name='Published')

    class Meta:
        verbose_name_plural = 'Team Profiles'

    def __str__(self):
        return self.name
