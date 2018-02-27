from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^login/$', auth_views.login, {'redirect_authenticated_user': True }, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),

    url(r'^entity/$', views.user_entity, name='user_entity'),
    url(r'^entity/add$', views.add_entity, name='add_entity'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/$', views.entity_detail, name='entity_detail'),
    url(r'^entity/(?P<pk>[0-9a-f-]+)/edit/$', views.entity_edit, name='entity_edit'),
    url(r'^entities/$', views.entity_list, name='entity_list'),

    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^profile/(?P<pk>[0-9a-f-]+)/$', views.profile_detail, name='profile_detail'),
    url(r'^users/search/$', views.search_users, name='search_users'),

    url(r'^categories/$', views.category_list, name='category_list'),
    url(r'^categories/add$', views.add_category, name='add_category'),
    url(r'^categories/(?P<pk>[0-9a-f-]+)/edit/$', views.category_edit, name='category_edit'),

    url(r'^dashboard/$', views.profile, name='dashboard'),
]