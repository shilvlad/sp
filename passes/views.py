
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponse
from django.conf import settings
from passes.forms import PassesForm
from passes.models import Passes, PassesUsers, PassesEmails
from django.contrib.auth.models import User
import datetime
from django.shortcuts import redirect
from django.core.mail import send_mail
import logging

applog = logging.getLogger('applog')
errorlog = logging.getLogger('errorlog')


# Create your views here.
@login_required
def start(request, pass_id=None):
    context = {}
    try:
        context['role'] = PassesUsers.objects.get(user=request.user.id).role
    except Exception:
        errorlog.critical('Ошибка ролевого доступа. КОНТЕКСТ: {user: %s}' % (request.user,))
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':

        if request.method == 'POST':

            form = PassesForm(request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                response.author = User.objects.get(username=request.user)
                response.save()

        if pass_id is None:
            context['form'] = PassesForm()
        else:
            context['form'] = PassesForm(instance=Passes.objects.get(id=pass_id))

        allPasses = Passes.objects.all().filter(deleted=False)

        warning_days = 120
        danger_days = 90
        critical_days = 30

        for i in allPasses:
            if i.author == request.user:
                i.showmy = True
            else:
                i.showmy = False
            try:
                i.days_left = (i.passexpired - datetime.date.today()).days
            except Exception:
                errorlog.critical('Возникло исключение при подсчете оставшихся до окончания '
                                  'пропуска дней. КОНТЕКСТ: {user: %s | pass: %s}' % (request.user, i))
            if i.days_left > warning_days:
                i.status = "table-success"

            elif i.days_left <= warning_days and i.days_left > danger_days+1:
                i.status = "table-warning"

            elif i.days_left <= danger_days and i.days_left > critical_days+1:
                i.status = "table-danger"

            else:
                i.status = "table-dark"

        #context['passes'] = allPasses
        context['passes'] = sorted(allPasses, key=lambda passes: passes.passexpired)


    if context['role'] == 'controller':


        allPasses = Passes.objects.all().filter(deleted=False)

        warning_days = 120
        danger_days = 90
        critical_days = 30

        for i in allPasses:
            if i.author == request.user:
                i.showmy = True
            else:
                i.showmy = False

            try:
                # i.days_left = int(str(i.passexpired - datetime.date.today()).split()[0])
                i.days_left = (i.passexpired - datetime.date.today()).days
            except Exception:
                errorlog.critical('Возникло исключение при подсчете оставшихся до окончания пропуска дней. КОНТЕКСТ: {user: %s | pass: %s}' % (request.user, i))

            if i.days_left > warning_days:
                i.status = "table-success"

            elif i.days_left <= warning_days and i.days_left > danger_days + 1:
                i.status = "table-warning"

            elif i.days_left <= danger_days and i.days_left > critical_days + 1:
                i.status = "table-danger"

            else:
                i.status = "table-dark"

        context['passes'] = sorted(allPasses, key=lambda passes: passes.passexpired)

    if context['role'] == 'admin':
        pass

    return render(request, 'passes/index.html', context)


@login_required
def delete_pass(request, pass_id):
    try:
        p = Passes.objects.get(id=pass_id)
        p.deleted = True
        p.save()


    except Exception:
        return HttpResponse("Что-то не то с ID пропуска: " + str(pass_id))

    return redirect('/passes/')

def check_passes(request):
    warning_days = 120
    danger_days = 90
    critical_days = 30

    passes = Passes.objects.all().filter(deleted=False).filter(passtype='mash')
    warning_passes = []
    msg = ''
    for i in passes:
        i.days_left = int(str(i.passexpired - datetime.date.today()).split()[0])
        if i.days_left <= warning_days and i.days_left > danger_days + 1:
            warning_passes.append(i)

    if warning_passes is not None:
        for i in warning_passes:
            msg += u'Пропуск: %s; ФИО: %s; Истекает: %s \n\n' % (i.passtype, str(i.owner), i.passexpired)
            applog.info('Истекающий срок действия: %s - %s - %s' % (i.passtype, str(i.owner), i.passexpired))
        emails = list(PassesEmails.objects.all().values_list('email', flat=True))
        for m in emails:
            send_mail(u'ВНИМАНИЕ! Истекают пропуска', msg, 'admin@portal.iteko.su', [m], fail_silently=False)

            applog.info('Информация о пропусках отправлена на адрес ' + m)

    return HttpResponse("OK")

