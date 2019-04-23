

#from django.contrib.auth.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),

    url(r'^record_delete/(?P<zip_record_id>[0-9]+)/$', views.record_delete, name='record_delete'),
    url(r'^freerecord_delete/(?P<zip_record_id>[0-9]+)/$', views.freerecord_delete, name='freerecord_delete'),
    url(r'^stationeryrecord_delete/(?P<zip_record_id>[0-9]+)/$', views.stationeryrecord_delete, name='freerecord_delete'),
    url(r'^to_order/(?P<order_id>[0-9]+)/$', views.to_order, name='to_order'),
    url(r'^export/excel', views.export_excel, name='export_excel'),

    url(r'^hide_order/(?P<order_id>[0-9]+)/$', views.hide_order, name='hide_order'),
    url(r'^close_order/(?P<order_id>[0-9]+)/$', views.close_order, name='close_order'),
    url(r'^reopen_order/(?P<order_id>[0-9]+)/$', views.reopen_order, name='reopen_order'),

    url(r'^add_zip/', views.add_zip, name='add_zip'),
    url(r'^add_freezip/', views.add_freezip, name='add_freezip'),
    url(r'^add_stationeryzip/', views.add_stationery, name='add_stationery'),

    url(r'^update_record/', views.update_record, name='update_record'),
    url(r'^update_comment/', views.update_comment, name='update_comment'),

    url(r'^idea/', views.idea, name='idea'),



#    url(r'^contacts/', views.contacts, name='contacts'),
#    url(r'^userrequest/', views.userrequest, name='userrequest'),
#    url(r'^login/', views.user_login, name='login'),
#    url(r'^logout/', views.user_logout, name='logout'),
#    url(r'^profile/', views.profile, name='profile'),

]
