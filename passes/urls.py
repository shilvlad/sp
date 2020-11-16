#from django.contrib.auth.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^(?P<pass_id>[0-9]+)$', views.start, name='start'),

    url(r'^delete_pass/(?P<pass_id>[0-9]+)/$', views.delete_pass, name='delete_pass'),
    url(r'^check_passes/$', views.check_passes, name='check_passes')
    #url(r'^roadsheet_delete/(?P<sheet_id>[0-9]+)/$', views.roadsheet_delete, name='roadsheet_delete'),
    ]