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
    order_temp = models.BooleanField(default=True)
    order_closed = models.BooleanField(default=False)
    date = models.DateTimeField(blank=True, editable=False, null=True)
    def get_ziprecords(self):
        try:
            tmp = ZipRecord.objects.filter(order=self)
        except Exception:
            tmp = None
        return tmp
    def __str__(self):
        return "Заказ № " + str(self.id) + " - Закрыт: " + str(self.order_closed) + ", заказчик: " + str(self.author)


class ZipRecord(models.Model):
    zip = models.ForeignKey(ZipNames, on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    order = models.ForeignKey(ZipOrder, on_delete=models.CASCADE, default=0)
    comment = models.CharField(max_length=500, editable = True, blank=True)
    def __str__(self):
        return str(self.id) + ". "+ str(self.zip) + " - " + str(self.amount) + " (Заказ: " + str(self.order) + ")"

