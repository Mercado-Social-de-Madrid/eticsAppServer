from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from currency.models import Entity


class BalanceDetail(DetailView):
    template_name = 'balance/detail.html'
    context_object_name = 'entity'

    def get_object(self, queryset=None):
        return Entity.objects.filter(member_id=self.kwargs['member_id']).first()

