from django.conf.urls import url
from . import views


urlpatterns = [
    #url(r'^$', views.new_offer, name='new_offer'),
    url(r'^entity/(?P<entity_pk>[0-9a-f-]+)/offers$', views.entity_offers, name='entity_offers'),
    url(r'^entity/(?P<entity_pk>[0-9a-f-]+)/offer/(?P<offer_pk>[0-9a-f-]+)$', views.offer_detail, name='offer_detail'),
    url(r'^entity/(?P<entity_pk>[0-9a-f-]+)/offer/(?P<offer_pk>[0-9a-f-]+)/edit$', views.offer_edit, name='offer_edit'),
    url(r'^entity/(?P<entity_pk>[0-9a-f-]+)/add_offer', views.add_offer, name='add_entity_offer'),

    url(r'^offers$', views.user_offers, name='user_offers'),
]