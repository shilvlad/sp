# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from passes.models import Passes, PassesUsers, PassesEmails
from django.contrib import admin

# Register your models here.
admin.site.register(PassesUsers)
admin.site.register(Passes)
admin.site.register(PassesEmails)
