# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.db import models

STATUS_PROCESSED = 'processed'
STATUS_CANCELLED = 'cancelled'
STATUS_PENDING = 'pending'
TRANSACTION_STATUS = (
    (STATUS_PROCESSED, 'Procesada'),
    (STATUS_CANCELLED, 'Cancelada'),
    (STATUS_PENDING, 'Pendiente'),
)


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    wallet_from = models.ForeignKey('currency.Wallet', blank=True, null=True, related_name='transactions_from')
    wallet_to = models.ForeignKey('currency.Wallet', related_name='transactions_to')
    amount = models.FloatField(default=0, verbose_name='Cantidad')
    concept = models.TextField(blank=True, null=True, verbose_name='Concepto')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    status = models.CharField(default=STATUS_PENDING, max_length=20, choices=TRANSACTION_STATUS, verbose_name='Estado')

    tax_processed = models.BooleanField(default=False, verbose_name='Impuestos procesados')
    made_byadmin = models.BooleanField(default=False, verbose_name='Realizada por admin')
    is_bonification = models.BooleanField(default=False, verbose_name='Bonificación')
    is_euro_purchase = models.BooleanField(default=False, verbose_name='Compra de euros')

    rel_transaction = models.ForeignKey('self', null=True, blank=True)
    comments = models.TextField(null=True, blank=True, verbose_name='Comentarios adicionales')

    class Meta:
        verbose_name = 'Transacción'
        verbose_name_plural = 'Transacciones'
        ordering = ['timestamp']
