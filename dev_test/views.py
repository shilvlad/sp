# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render, HttpResponseRedirect, HttpResponse

# Create your views here.
def start(request):
    context = {}
    return render(request, 'dev_test/index.html', context)
    #return HttpResponse("GOOD")