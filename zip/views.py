# -*- coding: utf-8 -*-

from django.shortcuts import render
from zip.forms import ZipRecordForm
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from zip.models import ZipNames, ZipRecord, ZipOrder
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
@login_required
def start(request):
    


    context = {}
    try:
        current_order = ZipOrder.objects.filter(order_temp=True).get(author=request.user)
    except Exception:
        tmp = ZipOrder()
        tmp.author = User.objects.get(username=request.user)
        tmp.save()
        current_order = ZipOrder.objects.filter(order_temp=True).get(author=request.user)

    ActualOrder = ZipRecord.objects.filter(order=current_order.id)
    PreviousOrders = ZipOrder.objects.filter(author=request.user).filter(order_temp=False).order_by("-date")[0:5]


    if request.method == 'POST':
        form = ZipRecordForm(request.POST)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/zip')
        else:
            print("непонятная ситуация")
    else:
        form = ZipRecordForm()
        form.fields['order'].queryset = ZipOrder.objects.filter(author=request.user).filter(order_temp=True)
        form.fields['order'].empty_label = None

    context['form'] = form
    context['order'] = ActualOrder
    context['prev_orders'] = PreviousOrders
    context['current_order'] = current_order.id
    return render(request, 'zip/index.html', context)

#TODO Проверить возможность удаления закрытых зипов через адресную строку
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
def to_order(request, order_id):
    try:
        tmp = ZipOrder.objects.get(id=order_id)
        print (tmp)
    except Exception:
        return HttpResponse("Мимо")

    if tmp.author == request.user and tmp.order_temp == True:
        tmp.order_temp = False
        tmp.date = datetime.datetime.now()
        tmp.save()

    else:
        return HttpResponse("Чужие заказы трогать низзя!")
    return HttpResponseRedirect('/zip')