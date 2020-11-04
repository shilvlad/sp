#from django.contrib.auth.urls import path
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.start, name='start'),
    url(r'^add_pass/', views.add_pass, name='add_pass'),
    ]