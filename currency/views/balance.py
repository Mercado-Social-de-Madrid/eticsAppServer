from django.shortcuts import get_object_or_404
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.generic import DetailView

from currency.models import Entity


class BalanceDetail(DetailView):
    template_name = 'balance/detail.html'
    context_object_name = 'entity'

    @xframe_options_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return Entity.objects.filter(member_id=self.kwargs['member_id']).first()

class EntityBalance(DetailView):

    template_name = 'balance/entity.html'
    context_object_name = 'entity'

    def get_object(self, queryset=None):
        return get_object_or_404(Entity, pk=self.kwargs['pk'])
