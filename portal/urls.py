
#from django.contrib.auth.urls import path
from django.conf.urls import include
from . import views
from django.urls import include, re_path
urlpatterns = [
    re_path(r'^$', views.start, name='start'),
#    url(r'^contacts/', views.contacts, name='contacts'),
#    url(r'^userrequest/', views.userrequest, name='userrequest'),
    re_path(r'^accounts/login/', views.user_login, name='login'),
    re_path(r'^accounts/logout/', views.user_logout, name='logout'),
    re_path(r'^accounts/chpwd/', views.user_chpwd, name='user_chpwd'),
#    url(r'^profile/', views.profile, name='profile'),

]
