# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
class ZipNames(models.Model):
    ZipName = models.CharField(max_length=300, editable = True)
    def __str__(self):
        return self.ZipName