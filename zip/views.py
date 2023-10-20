# -*- coding: utf-8 -*-

# codepage=UTF8

import datetime
import mimetypes
import os
import logging

import xlsxwriter
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.core import serializers

from zip.forms import ZipRecordForm, FreeZipRecordForm, StationeryRecordForm, ZipIdeaForm
from zip.models import ZipRecord, ZipOrder, ZipUsers, FreeZipRecord, StationeryRecord, ZipIdea

from django.core.mail import send_mail

applog = logging.getLogger('applog')
errorlog = logging.getLogger('errorlog')


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

        #TODO Обработку идей добавить
        #ideas = ZipIdea.objects.all()


        PreviousOrders = ZipOrder.objects.filter(author=request.user).filter(order_temp=False).order_by("-date")[0:5]

        if request.method == 'POST':

            errorlog.critical('Ошибка в главном виде. Method POST used. КОНТЕКСТ: {user: %s }' % (request.user))
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


    if context['role'] == 'admin':
        #send_mail(u'Вход в админку', u'Выполнен вход в администраторскую панель', 'ilya.schegolyaev@ramax.ru', [ 'ilya.schegolyaev@ramax.ru'], fail_silently=False, )
        pass

    return render(request, 'zip/index.html', context)

@login_required
def add_zip(request):
    applog = logging.getLogger('applog')
    errorlog = logging.getLogger('errorlog')
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

                if t.count() > 1:
                    a = t[0].amount.__int__() + t[1].amount.__int__()
                    n = ZipRecord.objects.get(id=t[0].id)
                    n.amount = a
                    n.save()

                    t[1].delete()
                return HttpResponseRedirect('/zip')
            else:

                errorlog.critical('form.is_valid in add_zip(). КОНТЕКСТ: {user: %s }' % (request.user))

        else:
            return HttpResponseRedirect('/zip')


    else:

        errorlog.critical('Not teamlead. КОНТЕКСТ: {user: %s }' % (request.user))
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

                if t.count() > 1:
                    a = t[0].amount.__int__() + t[1].amount.__int__()
                    n = FreeZipRecord.objects.get(id=t[0].id)
                    n.amount = a
                    n.save()

                    t[1].delete()
                return HttpResponseRedirect('/zip')
            else:
                errorlog.critical('form.is_valid in add_freezip(). КОНТЕКСТ: {user: %s }' % (request.user))

        else:
            return HttpResponseRedirect('/zip')


    else:

        errorlog.critical('Not teamlead. КОНТЕКСТ: {user: %s }' % (request.user))
        return HttpResponseRedirect('/zip')

@login_required
def add_stationery(request):
    context = {}
    try:
        context['role'] = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        errorlog.critical('Ошибка ролевого доступа. КОНТЕКСТ: {user: %s}' % (request.user))
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':
        if request.method == 'POST':
            form = StationeryRecordForm(request.POST)
            if form.is_valid():
                new_order = form.save()
                t = StationeryRecord.objects.filter(zip= new_order.zip,order=new_order.order, comment=new_order.comment)

                if t.count() > 1:
                    a = t[0].amount.__int__() + t[1].amount.__int__()
                    n = StationeryRecord.objects.get(id=t[0].id)
                    n.amount = a
                    n.save()

                    t[1].delete()
                return HttpResponseRedirect('/zip')
            else:
                errorlog.critical('form.is_valid in add_stationery. КОНТЕКСТ: {user: %s}' % (request.user))

        else:
            return HttpResponseRedirect('/zip')


    else:
        errorlog.critical('Not teamlead. КОНТЕКСТ: {user: %s }' % (request.user))
        return HttpResponseRedirect('/zip')

@login_required
def update_record(request):
    if request.method == 'POST':

        return HttpResponseRedirect('/zip')

    else:
        source = {}
        source['zip'] = ZipRecord
        source['freezip'] = FreeZipRecord
        source['stationery'] = StationeryRecord

        #print request.GET['type']
        tmp = source[request.GET['type']].objects.get(id = request.GET['id'])
        tmp.amount = request.GET['amount']
        tmp.save()

        data = serializers.serialize('xml', source[request.GET['type']].objects.filter(id = request.GET['id']), fields=('amount'))

        return HttpResponse(data)
        #return HttpResponseRedirect('/zip')

@login_required
def update_comment(request):
    if request.method == 'POST':
        #return HttpResponse(request.POST['id'])
        return HttpResponseRedirect('/zip')

    else:
        source = {}
        source['zip'] = ZipRecord
        source['freezip'] = FreeZipRecord
        source['stationery'] = StationeryRecord

        #print request.GET['type']
        tmp = source[request.GET['type']].objects.get(id = request.GET['id'])
        tmp.comment = request.GET['comment']
        #print tmp.comment
        tmp.save()

        data = serializers.serialize('xml', source[request.GET['type']].objects.filter(id = request.GET['id']), fields=('comment'))
        #print data
        return HttpResponse(data)
        #return HttpResponseRedirect('/zip')

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

    except Exception:
        errorlog.error("Ошибка исполнения ZipOrder.objects.get(id=order_id)")
        return HttpResponse("Мимо")
    if tmp.author == request.user and tmp.order_temp == True:
        tmp.order_temp = False
        tmp.date = datetime.datetime.now()
        tmp.save()
        applog.info(f'Создан заказ. КОНТЕКСТ: (User: %s, Номер заказа: %s)' % (request.user, tmp.id))

    else:
        return HttpResponse("Чужие заказы трогать низзя!")
    return HttpResponseRedirect('/zip')

@login_required
def close_order(request, order_id):
    try:
        tmp = ZipOrder.objects.get(id=order_id)
    except Exception:
        errorlog.error("Ошибка исполнения ZipOrder.objects.get(id=order_id)")
        return HttpResponse("Getting order Exception recieved")

    try:
        role = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        errorlog.critical("HIDE_ORDER. Критическая ошибка контроля ролей")
        return HttpResponse("HIDE_ORDER. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if tmp.order_closed == False and role == 'controller':
        tmp.order_closed = True
        tmp.order_hidden = False
        tmp.date_closed = datetime.datetime.now()
        tmp.save()

    else:
        errorlog.critical("Критическая ошибка скрытия заказа")
        return HttpResponse("Критическая ошибка скрытия заказа")
    return HttpResponseRedirect('/zip')

@login_required
def reopen_order(request, order_id):
    try:
        tmp = ZipOrder.objects.get(id=order_id)
    except Exception:
        errorlog.critical("Getting order Exception recieved")
        return HttpResponse("Getting order Exception recieved")

    try:
        role = ZipUsers.objects.get(user=request.user.id).role
    except Exception:
        errorlog.critical("HIDE_ORDER. Критическая ошибка контроля ролей. Обратитесь к администратору")
        return HttpResponse("HIDE_ORDER. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if tmp.order_closed == True and role == 'controller':
        tmp.order_closed = False
        tmp.order_hidden = False
        tmp.date_hidden = datetime.datetime.now()
        tmp.save()

    else:
        errorlog.critical("Критическая ошибка открытия заказа")
        return HttpResponse("Критическая ошибка открытия заказа")
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

# Сворачиваем список
def clean_list(list):
    zips_clean = []
    for a, b, c, d in (list):
        in_clean_list = False
        for ac, bc, cc, dc in (zips_clean):
            if ac == a and cc == c:
                in_clean_list = True
                zips_clean.remove([ac, bc, cc, dc])
                zips_clean.append([ac, b + bc, cc, dc])
                break

        if in_clean_list == False:
            zips_clean.append([a, b, c, d])
    return zips_clean

@login_required
def export_excel(request):
    excel_file_name = settings.BASE_DIR + "/tmp/temp.xls"

    try:
        role = ZipUsers.objects.get(user=request.user.id).role
    except Exception:

        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if role == 'controller':
        orders = ZipOrder.objects.filter(order_temp=False, order_closed=False, order_hidden=False)

    else:
        return HttpResponse("EXPORT_EXCEL. Не контролёр. Это неправильно. Обратитесь к администратору")

    zips = []
    for o in orders:
        zr = o.get_ziprecords()
        for zip in zr:
            zips.append([zip.zip.name, zip.amount, zip.comment, o.author])

        fzr = o.get_freeziprecords()
        for zip in fzr:
            zips.append([zip.zip, zip.amount, zip.comment, o.author])

        sr = o.get_stationeryrecords()
        for zip in sr:
            zips.append([zip.zip.name, zip.amount, zip.comment, o.author])

    # Group list
    groups = []
    for a,b,c,d in (zips):
        #print a,b,c,d
        if d not in groups:
            groups.append(d)

    zips_clean = clean_list(zips)

    # Списки по группам
    zips_by_group = {}
    for group in groups:
        zz = []
        for a, b, c ,d in (zips):
            if d == group:
                zz.append([a,b,c,d])
                #print d
        zips_by_group[str(group)] = clean_list(zz)

    # Общий список
    row = 0
    col = 0

    workbook = xlsxwriter.Workbook(excel_file_name)
    ws = workbook.add_worksheet("All")

    ws.write(row, col, 'ZIP_NAME')
    ws.write(row, col + 1, 'AMOUNT')
    ws.write(row, col + 2, 'COMMENT')
    row += 1

    for item, amount, comment, group in (zips_clean):
        ws.write(row, col, item)
        ws.write(row, col + 1, amount)
        ws.write(row, col + 2, comment)
        row += 1

    for g in groups:
        ws = workbook.add_worksheet(str(g))
        row = 0
        col = 0
        ws.write(row, col, 'ZIP_NAME')
        ws.write(row, col + 1, 'AMOUNT')
        ws.write(row, col + 2, 'COMMENT')
        row += 1

        for item, amount, comment, group in (zips_by_group[str(g)]):
            ws.write(row, col, item)
            ws.write(row, col + 1, amount)
            ws.write(row, col + 2, comment)
            row += 1

    ws = workbook.add_worksheet("Orders")
    row = 0
    ws.write(row, 0, 'Order')
    for oo in orders:
        row += 1
        ws.write(row, 0, oo.id)


    workbook.close()
    fp = open(excel_file_name, "rb");
    response = HttpResponse(fp.read());
    fp.close();

    # Download
    file_type = mimetypes.guess_type(excel_file_name);
    if file_type is None:
        file_type = 'application/octet-stream';
    response['Content-Type'] = file_type
    response['Content-Length'] = str(os.stat(excel_file_name).st_size);
    response['Content-Disposition'] = "attachment; filename=report.xlsx";
    os.remove(excel_file_name)


    return response

@login_required
def idea(request):
    context = {}
    if request.method == 'POST':
        form = ZipIdeaForm(request.POST)
        data = form.save(commit=False)
        data.author = User.objects.get(username=request.user)
        data.timestamp_create = datetime.datetime.now()
        data.save()

        return HttpResponse("<script>window.close();window.opener.location.reload();</script>")
    else:
        form = ZipIdeaForm()
        context['form'] = form

        return render(request, 'zip/idea.html', context)


@login_required
def idea_show(request):
    context = {}
    context['role'] = ZipUsers.objects.get(user=request.user.id).role
    ideas = ZipIdea.objects.all()
    context['ideas'] = ideas
    #print ideas
    return render(request, 'zip/idea_show.html', context)




