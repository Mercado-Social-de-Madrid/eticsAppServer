# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models

from currency.models import Entity

STATUS_ACCEPTED = 'accepted'
STATUS_CANCELLED = 'cancelled'
STATUS_PENDING = 'pending'
PAYMENT_STATUS = (
    (STATUS_ACCEPTED, 'Aceptado'),
    (STATUS_CANCELLED, 'Cancelado'),
    (STATUS_PENDING, 'Pendiente'),
)


class PaymentManager(models.Manager):

    def new_payment(self):
        return self.create(status=STATUS_PENDING)


class Payment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    processed = models.DateTimeField(auto_now_add=False, verbose_name='Timestamp procesado')
    user = models.ForeignKey(User)
    entity = models.ForeignKey(Entity)

    status = models.CharField(max_length=8, choices=PAYMENT_STATUS)
    total_amount = models.FloatField(default=0, verbose_name='Importe total')
    currency_amount = models.FloatField(default=0, verbose_name='Cantidad en boniatos')

    objects = PaymentManager()

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['user']


