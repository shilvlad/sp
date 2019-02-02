

#from django.contrib.auth.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^record_delete/(?P<zip_record_id>[0-9]+)/$', views.record_delete, name='record_delete'),
    url(r'^to_order/(?P<order_id>[0-9]+)/$', views.to_order, name='to_order'),
    url(r'^hide_order/(?P<order_id>[0-9]+)/$', views.hide_order, name='hide_order'),
    url(r'^close_order/(?P<order_id>[0-9]+)/$', views.close_order, name='close_order'),
#    url(r'^contacts/', views.contacts, name='contacts'),
#    url(r'^userrequest/', views.userrequest, name='userrequest'),
#    url(r'^login/', views.user_login, name='login'),
#    url(r'^logout/', views.user_logout, name='logout'),
#    url(r'^profile/', views.profile, name='profile'),

]
