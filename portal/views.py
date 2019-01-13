# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def start(request):
    return render(request, 'portal/index.html', {'username':request.user.username})

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
                return HttpResponseRedirect(next_url)
            else:
                return HttpResponse("Your account is disabled.")
        else:
            #TODO Добавить обработку неправильного логина/пароля
            #return HttpResponse("Invalid login details supplied.")
            return HttpResponseRedirect('/')
    else:
        context['next_url'] = next_url
        return render(request, 'portal/login.html', context)


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')