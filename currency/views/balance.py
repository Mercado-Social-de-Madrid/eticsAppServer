from django.shortcuts import get_object_or_404
from django.views.generic import DetailView

from currency.models import Entity


class BalanceDetail(DetailView):
    template_name = 'balance/detail.html'

    def get_object(self, queryset=None):
        return get_object_or_404(Entity, member_id=self.kwargs['member_id'])
