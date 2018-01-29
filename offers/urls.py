from django.conf.urls import url
from . import views


urlpatterns = [
    # url(r'^$', views.user_offers, name='user_offers'),
    #url(r'^$', views.new_offer, name='new_offer'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/offers$', views.entity_offers, name='entity_offers'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/add_offer', views.add_offer, name='add_entity_offer'),
]