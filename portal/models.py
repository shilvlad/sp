from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

class Applications(models.Model):
    name = models.CharField(max_length=20, editable=True)
    fullname = models.CharField(max_length=300, editable=True)
    def __unicode__(self):
        return self.name

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=1000, blank=True)
    apps = models.ManyToManyField(Applications, related_name= 'accessed_apps')
    #da = models.ForeignKey(Applications, on_delete=models.CASCADE, blank=True)

    def __unicode__(self):
        return self.user.username
    def get_apps(self):
        return self.objects.filter(user=self.user).values_list()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

