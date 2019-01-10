from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse




# Create your views here.
def start(request):
    return render(request, 'portal/index.html', {'username':request.user.username})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/zip')
            else:
                return HttpResponse("Your account is disabled.")
        else:
            print ("Invalid login details:")
            #TODO Добавить обработку неправильного логина/пароля
            #return HttpResponse("Invalid login details supplied.")
            return HttpResponseRedirect('/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')