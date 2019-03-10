# -*- coding: utf-8 -*-
from django.contrib import admin

# Register your models here.

from zip.models import ZipNames, ZipRecord, ZipOrder, ZipUsers, StationaryNames, StationeryRecord, ZipIdea

# Register your models here.
admin.site.register(ZipNames)
admin.site.register(ZipRecord)
admin.site.register(ZipOrder)
admin.site.register(ZipUsers)
admin.site.register(StationaryNames)
admin.site.register(ZipIdea)
