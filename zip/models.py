# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

# Create your models here.
class ZipNames(models.Model):
    name = models.CharField(max_length=300, editable = True)
    def __str__(self):
        return self.name

class ZipOrder(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    def __str__(self):
        return self.id


class ZipRecord(models.Model):
    zip = models.ForeignKey(ZipNames, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey(ZipOrder, on_delete=models.CASCADE, default=0)
    order_temp = models.BooleanField(default=False)
    def __str__(self):
        return str(self.zip) + " - " + str(self.amount) + " (" + str(self.author) + ")"

