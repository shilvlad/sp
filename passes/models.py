# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Passes(models.Model):
    PASS_TYPES = (
        ('afl', 'Пропуск АФЛ'),
        ('mash', 'Пропуск МАШ'),

    )

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.CharField(max_length=500, editable=True, blank=True)
    passexpired = models.DateField(blank=True, editable=True, null=True)
    passnumber = models.CharField(max_length=20, editable=True, blank=True)
    passtype = models.CharField(max_length=10, choices=PASS_TYPES)

    def get_passes(self):
        try:
            tmp = Passes.object.all()
        except Exception:
            tmp = None
        return tmp

    def __unicode__(self):
        desc = str(self.passtype) + " - " + str(self.passnumber) + " - " + str(self.passexpired)
        return desc



class PassesUsers(models.Model):
    ROLES_CHOICES = (
        ('teamlead', 'Руководитель группы'),
        ('controller', 'Контролер'),
        ('admin','Администратор')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLES_CHOICES)
    def __unicode__(self):
        return str(self.user) + " - " + str(self.role)