from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^payments$', views.pending_payments, name='pending_payments'),
    url(r'^payments/(?P<pk>[0-9a-f-]+)$', views.payment_detail, name='payment_detail'),

    url(r'^wallet/$', views.user_wallet, name='user_wallet'),

]