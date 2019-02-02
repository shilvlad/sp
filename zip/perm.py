# -*- coding: utf-8 -*-
from django.shortcuts import render
from zip.forms import ZipRecordForm
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from zip.models import ZipNames, ZipRecord, ZipOrder, ZipUsers
from django.contrib.auth.decorators import login_required
import datetime
import sp.settings


# Teamlead
def is_teamlead(req):

    try:
        zu = ZipUsers.objects.get(user=req.user.id)
        if zu.role == 'teamlead':
            return True
        else:
            return False

    except Exception:
        # TODO Вставить логирование
        return False

# Controller
def is_controller(req):
    try:
        zu = ZipUsers.objects.get(user=req.user.id)

        if zu.role == 'controller':
            return True
        else:
            return False

    except Exception:
        # TODO Вставить логирование
        return False

# ADMIN
def is_admin(req):
    try:
        zu = ZipUsers.objects.get(user=req.user.id)
        if zu.role == 'admin':
            return True
        else:
            return False

    except Exception:
            #TODO Вставить логирование
            return False



