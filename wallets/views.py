# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models.functions import TruncDay

import helpers
from helpers import superuser_required
from wallets.models import Payment, Wallet, TransactionLog, Transaction, WalletType
from django.utils import timezone

import datetime

@login_required
def pending_payments(request):
    pending_payments = Payment.objects.pending(user=request.user)

    page = request.GET.get('page')
    pending_payments = helpers.paginate(pending_payments, page, elems_perpage=10)
    params = {
        'payments': pending_payments
    }

    if request.is_ajax():
        response = render(request, 'wallets/payments_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/pending_payments.html', params)



@login_required
def payment_detail(request, pk):

    payment = get_object_or_404(Payment, pk=pk)
    can_edit = request.user == payment.receiver or request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para ver este pago')
        return redirect('entity_detail', pk=payment.pk )

    params = { 'payment': payment }

    if request.method == "POST":
        action = request.POST.get("action", "")

        if action == 'accept':
            try:
                payment.accept_payment()
                return redirect('pending_payments')
            except Wallet.NotEnoughBalance:
                params['notenoughbalance'] = True

        if action == 'cancel':
            payment.cancel_payment()
            return redirect('pending_payments')

    sender_type, sender = payment.sender.get_related_entity()
    receiver_type, entity = payment.receiver.get_related_entity()
    params['sender'] = sender
    params['bonus'] = entity.bonus(payment.total_amount, sender_type)

    return render(request, 'wallets/payment_detail.html', params)


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


@superuser_required
def admin_payments(request):
    payments = Payment.objects.all().order_by('-timestamp')

    page = request.GET.get('page')
    payments = helpers.paginate(payments, page, elems_perpage=10)
    params = {
        'payments': payments,
        'showing_all': True
    }

    if request.is_ajax():
        response = render(request, 'wallets/payments_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'wallets/admin_payments.html', params)

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
def wallet_types_list(request):

    wallet_types = WalletType.objects.all()
    return render(request, 'wallets/types_list.html', {'wallet_types':wallet_types})
