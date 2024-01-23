# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
import logging
from .models import Events, Profile
from supplies.models import SuppliesUsers

from django.contrib import messages

applog = logging.getLogger('applog')
errorlog = logging.getLogger('errorlog')

@login_required
def start(request):
    try:
        user = User.objects.get(id=request.user.id)
    except Exception:
        errorlog.critical("Error when checking user role")
    if user.is_superuser:
        context = {}
        context['events'] = Events.objects.all()
        context['role'] = 'admin'
        return render(request, 'portal/index.html', context)
    else:
        #В зависимости от пользовательских настроек переходим на дефолтную страницу
        try:
            defaultapp = Profile.objects.get(user=user).default_app
            print("Default app for user %s is %s" % (user, defaultapp))
            if not defaultapp:
                defaultapp = 'zip'

        except Exception as e:
            errorlog.critical(e)
            defaultapp = 'zip'

        return HttpResponseRedirect('/%s' % defaultapp)



def user_login(request):
    context = {}
    next_url = request.GET.get("next", "/")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                try:
                    user = User.objects.get(id=request.user.id)
                    print("User on login is: ", user)
                except Exception:
                    errorlog.critical("Error when checking user role")



                try:
                    #context['apps'] = list(Profile.objects.get(user=user).apps.all().values_list('name', flat=True))
                    request.session['apps'] = list(Profile.objects.get(user=user).apps.all().values_list('name', flat=True))
                    print("Applications on login are: ", request.session['apps'])
                except Exception as e:
                    errorlog.critical(e)
                    return HttpResponse("SUPPLIES. Критическая ошибка. Обратитесь к администратору")



                return HttpResponseRedirect(next_url)
            else:
                return HttpResponse("Your account is disabled.")
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
            return redirect('login')
    else:
        context['next_url'] = next_url
        return render(request, 'portal/login.html', context)


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

@login_required
def user_chpwd(request):
    u = User.objects.get(username=request.user)
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            old_password = request.POST.get("old_password")
            new_pass = request.POST.get("new_password")
            new_pass_rep = request.POST.get("new_password_repeat")
            if check_password(old_password, u.password):
                user = form.save()
                update_session_auth_hash(request, user)
                return render(request, 'zip/index.html')
            else:
                return render(request, 'portal/chpwd.html', {'form': form, 'user': u})
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'portal/chpwd.html',{'form': form, 'user': u})