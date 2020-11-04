# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.conf import settings
from passes.forms import PassesForm
from passes.models import Passes, PassesUsers
from django.contrib.auth.models import User

# Create your views here.
@login_required
def start(request):
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
                print (response.author)

        context['form'] = PassesForm()

        context['passes'] = Passes.objects.filter(author=request.user)



    if context['role'] == 'controller':
        pass

    if context['role'] == 'admin':
        pass

    return render(request, 'passes/index.html', context)


@login_required
def add_pass(request):
    pass