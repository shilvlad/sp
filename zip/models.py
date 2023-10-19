# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class ZipNames(models.Model):
    name = models.CharField(max_length=300, editable = True)
    def __str__(self):
        return self.name

class StationaryNames(models.Model):
    name = models.CharField(max_length=300, editable=True)
    def __str__(self):
        return self.name

class ZipOrder(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_temp = models.BooleanField(default=True)
    order_closed = models.BooleanField(default=False)
    order_hidden = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, editable=False, null=True)
    date_hidden = models.DateTimeField(blank=True, editable=False, null=True)
    date_closed = models.DateTimeField(blank=True, editable=False, null=True)

    def get_ziprecords(self):
        try:
            tmp = ZipRecord.objects.filter(order=self)
        except Exception:
            tmp = None
        return tmp
    def get_freeziprecords(self):
        try:
            tmp = FreeZipRecord.objects.filter(order=self)
        except Exception:
            tmp = None
        return tmp
    def get_stationeryrecords(self):
        try:
            tmp = StationeryRecord.objects.filter(order=self)
        except Exception:
            tmp = None
        return tmp
    def __str__(self):
        #return "Заказ № " + unicode(self.id) + " - Закрыт: " + unicode(self.order_closed) + ", заказчик: " + unicode(self.author)
        return str(self.id)

class ZipRecord(models.Model):
    zip = models.ForeignKey(ZipNames, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(ZipOrder, on_delete=models.CASCADE, default=0)
    comment = models.CharField(max_length=500, editable = True, blank=True)
    def __str__(self):
        return str(self.id) + ". " + str(self.zip) + " - " + str(self.amount)

class FreeZipRecord(models.Model):
    zip = models.CharField(max_length=500, editable = True, blank=True)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(ZipOrder, on_delete=models.CASCADE, default=0)
    comment = models.CharField(max_length=500, editable = True, blank=True)
    def __str__(self):
        return unicode(self.id) + ". " + unicode(self.zip) + " - " + unicode(self.amount)

class StationeryRecord(models.Model):
    zip = models.ForeignKey(StationaryNames, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(ZipOrder, on_delete=models.CASCADE, default=0)
    comment = models.CharField(max_length=500, editable=True, blank=True)

    def __str__(self):
        return unicode(self.id) + ". " + unicode(self.zip) + " - " + unicode(self.amount)

class ZipUsers(models.Model):
    ROLES_CHOICES = (
        ('teamlead', 'Руководитель группы'),
        ('controller', 'Контролер'),
        ('admin','Администратор')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, choices=ROLES_CHOICES)
    def __str__(self):
        return str(self.user) + " - " + str(self.role)

class ZipIdea(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, editable=False)
    topic = models.CharField(max_length=300, editable=True)
    body = models.TextField(max_length=30000, editable=True)
    timestamp_create = models.DateTimeField(blank=True, editable=False, null=True)

