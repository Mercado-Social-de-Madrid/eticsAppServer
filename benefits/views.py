import django_filters
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, UpdateView, CreateView, DetailView
from django_filters.views import FilterView

from benefits.forms.benefitform import BenefitForm
from benefits.models import Benefit
from currency.models import Entity
from helpers import FilterMixin
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin


class BenefitFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status']


class BenefitFilter(django_filters.FilterSet):
    search = SearchFilter(names=['entity__name', 'entity__address', 'entity__email', 'benefit_for_entities', 'benefit_for_members'], lookup_expr='in', label='Buscar...')
    o = LabeledOrderingFilter(fields=['entity__name',], field_labels={'entity__name':'Nombre de la entidad',})

    class Meta:
        model = Benefit
        form = BenefitFilterForm
        fields = ['includes_intercoop_members', 'active',]


class BenefitListView(LoginRequiredMixin, FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):
    model = Benefit
    queryset = Benefit.objects.all()
    objects_url_name = 'benefit_detail'
    template_name = 'benefits/list.html'
    ajax_template_name = 'benefits/query.html'
    filterset_class = BenefitFilter
    paginate_by = 7

    def get_queryset(self):
        queryset = super(BenefitListView, self).get_queryset()
        if not self.request.user.is_superuser:
            queryset = Benefit.objects.all()
        return queryset

    csv_filename = 'ventajas'
    available_fields = ['entity', 'active', 'published_date', 'benefit_for_entities', 'benefit_for_members',
                        'includes_intercoop_members', 'in_person', 'online', 'discount_code', 'discount_link_entities',
                        'discount_link_members']


class BenefitDetailView(LoginRequiredMixin, DetailView):
    model = Benefit
    template_name = 'benefits/detail.html'

    def get_context_data(self, **kwargs):
        context = super(BenefitDetailView, self).get_context_data(**kwargs)
        can_edit = self.request.user.is_superuser or self.request.user.is_staff
        context['entity'] = self.object.entity
        context['benefit'] = self.object
        context['can_edit'] = can_edit
        return context

    def get_object(self, queryset=None):
        if self.kwargs.get('pk'):
            return super(BenefitDetailView, self).get_object(queryset)
        else:
            type, entity = get_user_model().get_related_entity(self.request.user)
            return entity.benefit


class BenefitCreateView(LoginRequiredMixin, CreateView):
    model = Benefit
    form_class = BenefitForm
    template_name = 'benefits/edit.html'

    def get_context_data(self, **kwargs):
        context = super(BenefitCreateView, self).get_context_data(**kwargs)
        entity_pk = self.kwargs.get('entity_pk')
        if entity_pk:
            context['entity'] = get_object_or_404(Entity, pk=entity_pk)
        context['is_new'] = True
        context['ajax_url'] = reverse('entity_list') + '?filter=true'
        return context

    def get_success_url(self):
        return reverse('benefit_detail', kwargs={'pk': self.object.pk})


class BenefitUpdateView(LoginRequiredMixin, UpdateView):
    model = Benefit
    form_class = BenefitForm
    template_name = 'benefits/edit.html'

    def get_context_data(self, **kwargs):
        context = super(BenefitUpdateView, self).get_context_data(**kwargs)
        context['entity'] = self.object.entity
        context['is_new'] = False
        context['ajax_url'] = reverse('entity_list') + '?filter=true'
        return context

    def get_success_url(self):
        return reverse('benefit_detail', kwargs={'pk': self.object.pk})


class BenefitDeleteView(LoginRequiredMixin, DeleteView):
    model = Benefit
    success_url = reverse_lazy('list_benefits')
    template_name = 'benefits/delete.html'

