# -*- coding: utf-8 -*-

from django.shortcuts import render
from zip.forms import ZipRecordForm, FreeZipRecordForm, StationeryRecordForm
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from zip.models import ZipNames, ZipRecord, ZipOrder, ZipUsers, FreeZipRecord, StationeryRecord
from django.contrib.auth.decorators import login_required
import datetime
import perm

#TODO Реализовать логгирование
#TODO распечатывание, выгрузка в Excel данных о заказах
#TODO реализация функционала заказа специфических предметов
#TODO реализация страницы помощи с возможностью отправки идеи


@login_required
def start(request):

    context = {}
    try:
        context['role'] = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':
        try:
            current_order = ZipOrder.objects.filter(order_temp=True).get(author=request.user)
        except Exception:
            tmp = ZipOrder()
            tmp.author = User.objects.get(username=request.user)
            tmp.save()
            current_order = ZipOrder.objects.filter(order_temp=True).get(author=request.user)

        ZO = ZipRecord.objects.filter(order=current_order.id)
        FZO = FreeZipRecord.objects.filter(order=current_order.id)
        SO = StationeryRecord.objects.filter(order=current_order.id)

        PreviousOrders = ZipOrder.objects.filter(author=request.user).filter(order_temp=False).order_by("-date")[0:5]

        if request.method == 'POST':
            print "ERROR in main view. Method POST used"
        else:
            form = ZipRecordForm()
            form.fields['order'].queryset = ZipOrder.objects.filter(author=request.user).filter(order_temp=True)
            form.fields['order'].empty_label = None

            form_free = FreeZipRecordForm()
            form_free.fields['order'].queryset = ZipOrder.objects.filter(author=request.user).filter(order_temp=True)
            form_free.fields['order'].empty_label = None

            form_stationery = StationeryRecordForm()
            form_stationery.fields['order'].queryset = ZipOrder.objects.filter(author=request.user).filter(order_temp=True)
            form_stationery.fields['order'].empty_label = None

        context['form'] = form
        context['form_free'] = form_free
        context['form_stationery'] = form_stationery
        context['order'] = ZO
        context['freeorder'] = FZO
        context['stationeryorder'] = SO
        context['prev_orders'] = PreviousOrders

        context['current_order'] = current_order.id

    if context['role'] == 'controller':
        context['orders'] = ZipOrder.objects.filter(order_temp=False, order_closed=False, order_hidden=False).order_by("-date")
        context['orders_closed'] = ZipOrder.objects.filter(order_temp=False, order_closed=True, order_hidden=False).order_by("-date")
        context['orders_hidden'] = ZipOrder.objects.filter(order_temp=False, order_closed=True, order_hidden=True).order_by("-date")

    return render(request, 'zip/index.html', context)

@login_required
def add_zip(request):
    context = {}
    try:
        context['role'] = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':
        if request.method == 'POST':
            form = ZipRecordForm(request.POST)
            if form.is_valid():
                new_order = form.save()
                t = ZipRecord.objects.filter(zip= new_order.zip,order=new_order.order, comment=new_order.comment)
                #print t
                if t.count() > 1:
                    a = t[0].amount.__int__() + t[1].amount.__int__()
                    n = ZipRecord.objects.get(id=t[0].id)
                    n.amount = a
                    n.save()

                    t[1].delete()
                return HttpResponseRedirect('/zip')
            else:
                print("ERROR: form.is_valid in add_zip")
        else:
            return HttpResponseRedirect('/zip')


    else:
        print("ERROR: Not teamlead")
        return HttpResponseRedirect('/zip')

@login_required
def add_freezip(request):
    context = {}
    try:
        context['role'] = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':
        if request.method == 'POST':
            form = FreeZipRecordForm(request.POST)
            if form.is_valid():
                new_order = form.save()
                t = FreeZipRecord.objects.filter(zip= new_order.zip,order=new_order.order, comment=new_order.comment)
                #print t
                if t.count() > 1:
                    a = t[0].amount.__int__() + t[1].amount.__int__()
                    n = FreeZipRecord.objects.get(id=t[0].id)
                    n.amount = a
                    n.save()

                    t[1].delete()
                return HttpResponseRedirect('/zip')
            else:
                print("ERROR: form.is_valid in add_freezip")
        else:
            return HttpResponseRedirect('/zip')


    else:
        print("ERROR: Not teamlead")
        return HttpResponseRedirect('/zip')

@login_required
def add_stationery(request):
    context = {}
    try:
        context['role'] = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':
        if request.method == 'POST':
            form = StationeryRecordForm(request.POST)
            if form.is_valid():
                new_order = form.save()
                t = StationeryRecord.objects.filter(zip= new_order.zip,order=new_order.order, comment=new_order.comment)
                #print t
                if t.count() > 1:
                    a = t[0].amount.__int__() + t[1].amount.__int__()
                    n = StationeryRecord.objects.get(id=t[0].id)
                    n.amount = a
                    n.save()

                    t[1].delete()
                return HttpResponseRedirect('/zip')
            else:
                print("ERROR: form.is_valid in add_stationery")
        else:
            return HttpResponseRedirect('/zip')


    else:
        print("ERROR: Not teamlead")
        return HttpResponseRedirect('/zip')


@login_required
def record_delete(request, zip_record_id):
    try:
        tmp = ZipRecord.objects.get(id=zip_record_id)
    except Exception:
        return HttpResponse("Мимо")

    if tmp.order.author == request.user and tmp.order.order_temp == True:
        tmp.delete()
    else:
        return HttpResponse("Чужие заказы трогать низзя!")
    return HttpResponseRedirect('/zip')

@login_required
def freerecord_delete(request, zip_record_id):
    try:
        tmp = FreeZipRecord.objects.get(id=zip_record_id)
    except Exception:
        return HttpResponse("Мимо")

    if tmp.order.author == request.user and tmp.order.order_temp == True:
        tmp.delete()
    else:
        return HttpResponse("Чужие заказы трогать низзя!")
    return HttpResponseRedirect('/zip')

@login_required
def stationeryrecord_delete(request, zip_record_id):
    try:
        tmp = StationeryRecord.objects.get(id=zip_record_id)
    except Exception:
        return HttpResponse("Мимо")

    if tmp.order.author == request.user and tmp.order.order_temp == True:
        tmp.delete()
    else:
        return HttpResponse("Чужие заказы трогать низзя!")
    return HttpResponseRedirect('/zip')

@login_required
def to_order(request, order_id):
    try:
        tmp = ZipOrder.objects.get(id=order_id)
        #print (tmp)
    except Exception:
        return HttpResponse("Мимо")

    if tmp.author == request.user and tmp.order_temp == True:
        tmp.order_temp = False
        tmp.date = datetime.datetime.now()
        tmp.save()

    else:
        return HttpResponse("Чужие заказы трогать низзя!")
    return HttpResponseRedirect('/zip')

@login_required
def close_order(request, order_id):
    try:
        tmp = ZipOrder.objects.get(id=order_id)
        #print (tmp)
    except Exception:
        return HttpResponse("Getting order Exception recieved")

    try:
        role = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("HIDE_ORDER. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if tmp.order_closed == False and role == 'controller':
        tmp.order_closed = True
        tmp.order_hidden = False
        tmp.date_hidden = datetime.datetime.now()
        tmp.save()

    else:
        return HttpResponse("Критическая ошибка скрытия заказа")
    return HttpResponseRedirect('/zip')

@login_required
def hide_order(request, order_id):
    try:
        tmp = ZipOrder.objects.get(id=order_id)
        #print (tmp)
    except Exception:
        return HttpResponse("Getting order Exception recieved")

    try:
        role = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("HIDE_ORDER. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if tmp.order_hidden == False and role == 'controller':
        tmp.order_closed = True
        tmp.order_hidden = True
        tmp.date_hidden = datetime.datetime.now()
        tmp.save()

    else:
        return HttpResponse("Критическая ошибка скрытия заказа")
    return HttpResponseRedirect('/zip')

