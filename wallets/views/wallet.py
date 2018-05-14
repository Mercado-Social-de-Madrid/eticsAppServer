# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import TruncDay

import helpers
from helpers import superuser_required
from wallets.models import Payment, Wallet, TransactionLog, Transaction, WalletType
from django.utils import timezone

import datetime
@superuser_required
def wallet_types_list(request):

    wallet_types = WalletType.objects.all()
    return render(request, 'wallets/types_list.html', {'wallet_types':wallet_types})



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
