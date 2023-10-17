

#from django.contrib.auth.urls import path
from django.conf.urls import include
from . import views
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^$', views.start, name='start'),

    re_path(r'^record_delete/(?P<zip_record_id>[0-9]+)/$', views.record_delete, name='record_delete'),
    re_path(r'^freerecord_delete/(?P<zip_record_id>[0-9]+)/$', views.freerecord_delete, name='freerecord_delete'),
    re_path(r'^stationeryrecord_delete/(?P<zip_record_id>[0-9]+)/$', views.stationeryrecord_delete, name='freerecord_delete'),
    re_path(r'^to_order/(?P<order_id>[0-9]+)/$', views.to_order, name='to_order'),
    re_path(r'^export/excel', views.export_excel, name='export_excel'),

    re_path(r'^hide_order/(?P<order_id>[0-9]+)/$', views.hide_order, name='hide_order'),
    re_path(r'^close_order/(?P<order_id>[0-9]+)/$', views.close_order, name='close_order'),
    re_path(r'^reopen_order/(?P<order_id>[0-9]+)/$', views.reopen_order, name='reopen_order'),

    re_path(r'^add_zip/', views.add_zip, name='add_zip'),
    re_path(r'^add_freezip/', views.add_freezip, name='add_freezip'),
    re_path(r'^add_stationeryzip/', views.add_stationery, name='add_stationery'),

    re_path(r'^update_record/', views.update_record, name='update_record'),
    re_path(r'^update_comment/', views.update_comment, name='update_comment'),

    re_path(r'^idea/', views.idea, name='idea'),
    re_path(r'^idea_show/', views.idea_show, name='idea_show'),



#    url(r'^contacts/', views.contacts, name='contacts'),
#    url(r'^userrequest/', views.userrequest, name='userrequest'),
#    url(r'^login/', views.user_login, name='login'),
#    url(r'^logout/', views.user_logout, name='logout'),
#    url(r'^profile/', views.profile, name='profile'),

]
