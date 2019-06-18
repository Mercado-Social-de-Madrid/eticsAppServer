from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^offers/$', views.offers, name='offers'),

]