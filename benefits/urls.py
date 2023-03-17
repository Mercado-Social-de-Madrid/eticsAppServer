
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^benefits$', views.BenefitListView.as_view(), name='list_benefits'),
    url(r'^benefit/add$', views.BenefitCreateView.as_view(), name='add_benefit'),
    url(r'^entity/(?P<entity_pk>[0-9a-f-]+)/add_benefit', views.BenefitCreateView.as_view(), name='add_entity_benefit'),
    url(r'^benefit/(?P<pk>[0-9a-f-]+)/$', views.BenefitDetailView.as_view(), name='benefit_detail'),
    url(r'^benefit/(?P<pk>[0-9a-f-]+)/edit$', views.BenefitUpdateView.as_view(), name='benefit_edit'),
    url(r'^benefit/(?P<pk>[0-9a-f-]+)/delete', views.BenefitDeleteView.as_view(), name='benefit_delete'),
]