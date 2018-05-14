# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

import helpers
from helpers import superuser_required
from wallets.models import Payment, Wallet


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
                if request.is_ajax():
                    return JsonResponse({'success':True})
                else:
                    return redirect('pending_payments')
            except Wallet.NotEnoughBalance:
                params['notenoughbalance'] = True
                if request.is_ajax():
                    response = JsonResponse({'error':'notenoughbalance', 'error_message':'El monedero no tiene saldo suficiente.'})
                    response.status_code = 400
                    return response

        if action == 'cancel':
            payment.cancel_payment()
            if request.is_ajax():
                return JsonResponse({'success': True})
            else:
                return redirect('pending_payments')

    sender_type, sender = payment.sender.get_related_entity()
    receiver_type, entity = payment.receiver.get_related_entity()
    params['sender'] = sender
    if receiver_type == 'entity':
        params['bonus'] = entity.bonus(payment.total_amount, sender_type)

    return render(request, 'wallets/payment_detail.html', params)


@login_required
def new_payment(request, pk):

    payment = get_object_or_404(Payment, pk=pk)
    can_edit = request.user == payment.receiver or request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para ver este pago')
        return redirect('entity_detail', pk=payment.pk )

    if request.method == "POST":
        action = request.POST.get("action", "")

        if action == 'accept':
            payment.accept_payment()
            return redirect('pending_payments')

        if action == 'cancel':
            payment.cancel_payment()
            return redirect('pending_payments')

    else:
        sender_type, sender = payment.sender.get_related_entity()
        receiver_type, entity = payment.receiver.get_related_entity()

        bonus = entity.bonus(payment.total_amount, sender_type)
        return render(request, 'wallets/payment_detail.html', {
            'payment': payment,
            'bonus': bonus,
            'sender': sender
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