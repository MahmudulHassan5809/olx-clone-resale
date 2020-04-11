from django.db import models
from django.template.defaultfilters import truncatechars
# Create your models here.


class FeedBack(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)

    message = models.TextField()

    @property
    def short_description(self):
        return truncatechars(self.message, 35)

    def __str__(self):
        return 'Feedback'


class Contact(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phone_number = models.CharField(max_length=200)
    ad_url = models.URLField(max_length=200)

    message = models.TextField()

    @property
    def short_description(self):
        return truncatechars(self.message, 35)

    def __str__(self):
        return 'Contact'


class Terms(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()

    class Meta:
        verbose_name = 'Terms'
        verbose_name_plural = 'Terms'

    @property
    def short_description(self):
        return truncatechars(self.description, 35)

    def __str__(self):
        return self.name


class Setting(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=230)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    facebook_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    flickr_url = models.URLField(max_length=200, null=True, blank=True)
    googleplus_url = models.URLField(max_length=200, null=True, blank=True)

    sologan = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
