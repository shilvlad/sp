from django.contrib import admin
from django.urls import re_path
from django.views.generic import RedirectView
from django.urls import include, path

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'', include('portal.urls')),
    re_path(r'^zip/', include('zip.urls')),
    re_path(r'^passes/', include('passes.urls')),
    re_path(r'^supplies/', include('supplies.urls')),
    re_path(r'^dev_test/', include('dev_test.urls')),
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/icons/favicon.ico'))
]
