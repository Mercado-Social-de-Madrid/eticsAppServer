# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from wallets.models import Payment


@login_required
def pending_payments(request):
    pending_payments = Payment.objects.pending(user=request.user)
    return render(request, 'wallets/pending_payments.html', {
        'pending_payments': pending_payments
    })


@login_required
def payment_detail(request, pk):
    pending_payments = Payment.objects.pending(user=request.user)
    return render(request, 'wallets/pending_payments.html', {
        'pending_payments': pending_payments
    })
