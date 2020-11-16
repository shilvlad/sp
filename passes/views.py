# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from passes.forms import PassesForm
from passes.models import Passes, PassesUsers
from django.contrib.auth.models import User
import datetime
from django.shortcuts import redirect
from django.core.urlresolvers import reverse

# Create your views here.
@login_required
def start(request, pass_id=None):
    context = {}
    try:
        context['role'] = PassesUsers.objects.get(user=request.user.id).role
    except Exception:
        return HttpResponse("START. Критическая ошибка контроля ролей. Обратитесь к администратору")

    if context['role'] == 'teamlead':

        if request.method == 'POST':
            # Если сабмит, то добавляем пропуск и говорим что добавили
            form = PassesForm(request.POST)
            if form.is_valid():
                response = form.save(commit=False)
                response.author = User.objects.get(username=request.user)
                response.save()



        if pass_id == None:
            context['form'] = PassesForm()
        else:
            context['form'] = PassesForm(instance=Passes.objects.get(id=pass_id))


        context['passes'] = Passes.objects.all().filter(deleted=False)

        warning_days = 120
        danger_days = 90
        critical_days = 30

        for i in context['passes']:
            print(i.passexpired)
            i.days_left = int(str(i.passexpired - datetime.date.today()).split()[0])

            if i.days_left > warning_days:
                i.status = "table-success"

            elif i.days_left <= warning_days and i.days_left > danger_days+1:
                i.status = "table-warning"

            elif i.days_left <= danger_days and i.days_left > critical_days+1:
                i.status = "table-danger"

            else:
                i.status = "table-dark"

    if context['role'] == 'controller':
        pass

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
    #return redirect(reverse('start'))
    return redirect('/passes/')