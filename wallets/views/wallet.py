# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

import django_filters
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import TruncDay
from django.urls import reverse
from django.utils.decorators import method_decorator
from django_filters.views import FilterView
from filters.views import FilterMixin

import helpers
from helpers import superuser_required
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from wallets.models import Payment, Wallet, TransactionLog, Transaction, WalletType
from django.utils import timezone

import datetime
@superuser_required
def wallet_types_list(request):

    wallet_types = WalletType.objects.all()
    return render(request, 'wallets/types_list.html', {'wallet_types':wallet_types})


class WalletFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'type', ]


class WalletFilter(django_filters.FilterSet):

    search = SearchFilter(names=[ 'user__username', 'user__entity__name', 'user__person__name', 'user__person__surname', 'user__email'], lookup_expr='in',
                          label='Buscar...')
    o = LabeledOrderingFilter(fields=['last_transaction', 'balance'], field_labels={'last_transaction':'Última transacción','balance':'Saldo'})
    class Meta:
        model = Wallet
        form = WalletFilterForm
        fields = [ 'type' ]


@method_decorator(superuser_required, name='dispatch')
class WalletListView(FilterMixin, FilterView, ExportAsCSVMixin, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Wallet
    queryset = Wallet.objects.filter(user__isnull=False).order_by('-last_transaction')
    objects_url_name = 'wallet_detail'
    template_name = 'wallets/list.html'
    ajax_template_name = 'wallets/query.html'
    filterset_class = WalletFilter
    paginate_by = 10
    csv_filename = 'monederos'
    available_fields = ['user', 'user_full_name', 'is_registered', 'balance', 'last_transaction', 'type']
    field_labels = {
        'user': 'Nombre de usuario',
        'user_full_name': 'Nombre y apellidos',
        'type': 'Tipo monedero',
        'is_registered': 'Registrada',
    }

    def get_template_names(self):
        template_names = super(WalletListView, self).get_template_names()
        if self.request.is_ajax() and self.request.GET.get('filter', None) is not None:
            template_names = ['wallets/search.html'] + template_names

        return template_names


@superuser_required
def wallet_detail(request, pk):

    wallet = get_object_or_404(Wallet, pk=pk)
    user_type, instance = wallet.user.get_related_entity()
    transactions = TransactionLog.objects.filter(wallet=wallet)
    page = request.GET.get('page')
    transactions = helpers.paginate(transactions, page, elems_perpage=10)
    sent_pending_payments = Payment.objects.sent_pending(user=wallet.user)
    pending_payments = Payment.objects.pending(user=wallet.user)

    if request.is_ajax():
        response = render(request, 'wallets/transaction_logs_query.html', {'transactions':transactions})
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:

        start_date = timezone.now() - datetime.timedelta(days=71)
        end_date = timezone.now()

        transactions_bydate = TransactionLog.objects.filter(wallet=wallet,
                                                        timestamp__gte=start_date,
                                                         timestamp__lte=end_date) \
            .annotate(day=TruncDay('timestamp')) \
            .values('day') \
            .annotate(total=Sum('amount')).order_by('day')

        return render(request, 'wallets/detail.html', {
            'showing_all': False, 'instance':instance, 'user_type':user_type,
            'wallet': wallet, 'transactions': transactions,'transactions_bydate':transactions_bydate,
            'pending_payments': pending_payments, 'sent_pending_payments': sent_pending_payments
        })


@login_required
def user_wallet(request):

    pending_payments = Payment.objects.pending(user=request.user)
    wallet = Wallet.objects.filter(user=request.user).first()
    transactions = TransactionLog.objects.filter(wallet=wallet)
    page = request.GET.get('page')
    transactions = helpers.paginate(transactions, page, elems_perpage=10)

    if request.is_ajax():
        response = render(request, 'wallets/transaction_logs_query.html', {'transactions':transactions})
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/user_wallet.html', {
            'pending_payments': pending_payments,
            'showing_all': False,
            'wallet': wallet, 'transactions': transactions
        })

