
#from django.contrib.auth.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
#    url(r'^contacts/', views.contacts, name='contacts'),
#    url(r'^userrequest/', views.userrequest, name='userrequest'),
    url(r'^accounts/login/', views.user_login, name='login'),
    url(r'^accounts/logout/', views.user_logout, name='logout'),
    url(r'^accounts/chpwd/', views.user_chpwd, name='user_chpwd'),
#    url(r'^profile/', views.profile, name='profile'),

]
