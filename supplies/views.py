from django.shortcuts import render

from .models import SuppliesUsers, SupplyRemain, SupplyName, SuppliesGroup, IssueSupply
from portal.models import Profile
from django.shortcuts import render, HttpResponseRedirect, HttpResponse
import logging
from django.contrib.auth.decorators import login_required
from .forms import IssueSupplyForm
from django.contrib.auth.models import User

applog = logging.getLogger('applog')
errorlog = logging.getLogger('errorlog')

@login_required
def start(request):
    context = {}
    try:
        context['role'] = SuppliesUsers.objects.get(user=request.user.id).role
    except Exception as e:
        errorlog.critical(e)
        return HttpResponse("SUPPLIES. Критическая ошибка. Обратитесь к администратору")

    # Вьюшка для РГ или сотрудника
    if context['role'] == 'employee' or context['role'] == 'teamlead':
        try:
            context['group'] = SuppliesUsers.objects.get(user=request.user.id).group
            context['cartridges'] = list(SupplyRemain.objects.filter(group=context['group']))
            context['last_issues'] = IssueSupply.objects.filter(group=context['group']).order_by("-timestamp_created")[0:5]
        except Exception as e:
            errorlog.critical(e)
            return HttpResponse("SUPPLIES. Не удалось получить список выдач. Обратитесь к администратору", e)

        return render(request, 'supplies/index.html', context)

    # Вьюшка для контролера
    if context['role'] == 'controller':
        return render(request, 'supplies/controller.html', context)

    # Вьюшка для админа
    if context['role'] == 'admin':
        return render(request, 'supplies/admin.html', context)




#================================================
# Оформление выдачи расходного материала
@login_required
def issuesupply(request, remain_id):
    context = {}
    context['remain_id'] = remain_id
    if request.method == 'POST':
        form = IssueSupplyForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.user = User.objects.get(username=request.user)
            f.group = SuppliesUsers.objects.get(user=request.user.id).group
            f.supply = SupplyRemain.objects.get(id=remain_id)
            # TODO Не забыть вписать уменьшение количества
            f.save()
            return HttpResponseRedirect('/supplies')
    else:
        form = IssueSupplyForm()
        context['form'] = form
        try:
            context['role'] = SuppliesUsers.objects.get(user=request.user.id).role
            context['group'] = SuppliesUsers.objects.get(user=request.user.id).group
            context['last_issues'] = IssueSupply.objects.filter(group=context['group']).order_by(
                "-timestamp_created")
            context['last_issues'] = IssueSupply.objects.filter(group=context['group']).order_by("-timestamp_created")[
                                     0:5]
        except Exception as e:
            errorlog.critical(e)
            return HttpResponse("SUPPLIES. Не удалось получить список выдач. Обратитесь к администратору", e)

    return render(request, 'supplies/index_issue_supply.html', context)


#================================================
# Вывод истории замен по группе
@login_required
def history(request):
    context = {}

    try:
        context['role'] = SuppliesUsers.objects.get(user=request.user.id).role
    except Exception as e:
        errorlog.critical(e)
        return HttpResponse("SUPPLIES. Критическая ошибка. Обратитесь к администратору")

    if context['role'] == 'employee' or context['role'] == 'teamlead':
        try:
            context['group'] = SuppliesUsers.objects.get(user=request.user.id).group
        except Exception as e:
            errorlog.critical(e)
            return HttpResponse("SUPPLIES. Критическая ошибка получения группы из БД. Обратитесь к администратору", e)

        try:
            context['cartridges'] = list(SupplyRemain.objects.filter(group=context['group']))

        except Exception as e:
            errorlog.critical(e)
            return HttpResponse("SUPPLIES. Не удалось получить остатки. Обратитесь к администратору", e)

        try:
            context['last_issues'] = IssueSupply.objects.filter(group=context['group']).order_by("-timestamp_created")

        except Exception as e:
            errorlog.critical(e)
            return HttpResponse("SUPPLIES. Не удалось получить список выдач. Обратитесь к администратору", e)

        return render(request, 'supplies/history.html', context)





