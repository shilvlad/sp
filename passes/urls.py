#from django.contrib.auth.urls import path
from django.conf.urls import include
from . import views
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^$', views.start, name='start'),
    re_path(r'^(?P<pass_id>[0-9]+)$', views.start, name='start'),

    re_path(r'^delete_pass/(?P<pass_id>[0-9]+)/$', views.delete_pass, name='delete_pass'),
    re_path(r'^check_passes/$', views.check_passes, name='check_passes')
    #url(r'^roadsheet_delete/(?P<sheet_id>[0-9]+)/$', views.roadsheet_delete, name='roadsheet_delete'),
    ]