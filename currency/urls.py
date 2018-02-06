from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login/$', auth_views.login, {'redirect_authenticated_user': True }, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^entity/$', views.user_entity, name='user_entity'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/$', views.entity_detail, name='entity_detail'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/edit/$', views.entity_edit, name='entity_edit'),

    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^profile/(?P<pk>[0-9a-f-]+)/$', views.profile_detail, name='profile_detail'),

    url(r'^dashboard/$', views.profile, name='dashboard'),
]