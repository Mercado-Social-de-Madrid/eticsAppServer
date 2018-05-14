
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

from django.db.models import Sum
from django.db.models.functions import TruncDay
from django.shortcuts import render
from django.utils import timezone

import helpers
from helpers import superuser_required
from wallets.models import Transaction


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
