from django.conf.urls import url
from . import views


urlpatterns = [

    url(r'^news/$', views.news_list, name='news_list'),
    url(r'^news/add/$', views.add_news, name='add_news'),
 #   url(r'^news/(?P<pk>[0-9a-f-]+)$', views.news_detail, name='entity_offers'),
    url(r'^news/(?P<pk>[0-9a-f-]+)/edit/$', views.news_edit, name='news_edit'),
    url(r'^news/(?P<pk>[0-9a-f-]+)/delete/$', views.news_delete, name='news_delete'),

]