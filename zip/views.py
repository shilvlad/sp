from django.shortcuts import render
from zip.forms import ZipRecordForm
from django.shortcuts import render
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User



#    zip = models.ForeignKey(ZipNames, on_delete=models.CASCADE)
#    amount = models.IntegerField(default=0)
#    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#    order = models.ForeignKey(ZipOrder, on_delete=models.CASCADE, default=0)


# Create your views here.
def start(request):
    context = {}


    if request.method == 'POST':
        form = ZipRecordForm(request.POST)
    else:
        form = ZipRecordForm()
        form.fields['author'].queryset = User.objects.filter(username=request.user)
        form.fields['author'].empty_label = None



    context['form'] = form
    return render(request, 'zip/index.html', context)
