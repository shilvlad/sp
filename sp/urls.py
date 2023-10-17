"""sp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.urls import path,
#from django.conf.urls import include
from django.urls import re_path
from django.views.generic import RedirectView
from django.urls import include, path



urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    #url(r'^admin/', admin.site.urls),
    re_path(r'', include('portal.urls')),
    re_path(r'^zip/', include('zip.urls')),
    re_path(r'^passes/', include('passes.urls')),
    re_path(r'^dev_test/', include('dev_test.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico'))
]
