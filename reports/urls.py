from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^wallets/$', views.wallets, name='wallets'),
    url(r'^offers/$', views.offers, name='offers'),
    url(r'^entities/$', views.entities, name='entities'),
]