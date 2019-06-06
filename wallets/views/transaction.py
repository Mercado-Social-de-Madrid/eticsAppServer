
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

import helpers
from helpers import superuser_required
from wallets.forms.TransactionForm import TransactionForm
from wallets.models import Transaction, Wallet


@superuser_required
def transaction_list(request):

    start_date = timezone.now() - datetime.timedelta(days=71)
    end_date = timezone.now()

    transactions = Transaction.objects.all().order_by('-timestamp')
    transactions_bydate = Transaction.objects.filter(timestamp__gte=start_date,
                                                  timestamp__lte=end_date) \
                                        .annotate(day=TruncDay('timestamp')) \
                                      .values('day') \
                                      .annotate(total=Sum('amount')).order_by('day')


    page = request.GET.get('page')
    transactions = helpers.paginate(transactions, page, elems_perpage=10)
    params = {
        'transactions': transactions,
    }

    if request.is_ajax():
        response = render(request, 'wallets/transactions_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['transactions_bydate'] = transactions_bydate
        return render(request, 'wallets/transactions_list.html', params)



@superuser_required
def new_transaction(request):

    params = {
        'ajax_url': reverse('admin_wallet'),
    }

    if request.method == "POST":
        form = TransactionForm(request.POST, request.FILES)

        if form.is_valid():
            transaction = form.save(commit=False)
            wallet_from = transaction.wallet_from


            success = True
            try:
                t = wallet_from.new_transaction(
                    transaction.amount,
                    wallet=transaction.wallet_to,
                    concept=transaction.concept,
                    bonus=transaction.is_bonification,
                    made_byadmin=True,
                    is_euro_purchase=False,
                )
                transaction.wallet_to.notify_transaction(t)

            except Wallet.NotEnoughBalance:
                params['notenoughbalance'] = True
                params['wallet_from_display'] = wallet_from.user.get_related_entity()[1]
                params['wallet_to_display'] = transaction.wallet_to.user.get_related_entity()[1] if transaction.wallet_to.user else 'Débito'
                success = False

            if success:
                return redirect('transaction_list')
        else:
            print form.errors.as_data()
    else:
        form = TransactionForm()

    params['form'] = form
    return render(request, 'wallets/new_transaction.html', params)
