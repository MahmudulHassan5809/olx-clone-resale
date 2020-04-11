from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User


# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(
        upload_to="profile/%Y/%m/%d/", default="profile/default.png")
    phone_number = models.CharField(max_length=15, default='01xxxxxxxxxx')
    city = models.CharField(default='Your city', max_length=255)
    email_confirmed = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    try:
        if created:
            Profile.objects.create(user=instance)
        else:
            instance.user_profile.save()
    except Exception as e:
        pass
