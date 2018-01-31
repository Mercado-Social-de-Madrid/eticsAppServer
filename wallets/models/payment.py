# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models, transaction

from currency.models import Entity
from wallets.models import Wallet

STATUS_ACCEPTED = 'accepted'
STATUS_CANCELLED = 'cancelled'
STATUS_PENDING = 'pending'
PAYMENT_STATUS = (
    (STATUS_ACCEPTED, 'Aceptado'),
    (STATUS_CANCELLED, 'Cancelado'),
    (STATUS_PENDING, 'Pendiente'),
)


class PaymentManager(models.Manager):

    def new_payment(self, user, entity, total_amount, currency_amount=0):

        #TODO: Check that the user has enough currency in her wallet and no more than the max currency percent

        return self.create(
            user=user,
            entity=entity,
            total_amount=total_amount,
            currency_amount=currency_amount,
            status=STATUS_PENDING)



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

    @transaction.atomic
    def accept_payment(self):

        if self.status != STATUS_PENDING:
            return
            #TODO: create exception

        wallet_entity = Wallet.objects.filter(user=self.entity.user).first()
        wallet_user = Wallet.objects.filter(user=self.user).first()

        if not wallet_entity or not wallet_user:
            return
            # TODO: create exception

        #We calculate the bonification to give the user
        bonification = self.total_amount * self.entity.bonification_percent
        if bonification > 0:
            t = wallet_entity.new_transaction(bonification, wallet=wallet_user, bonification=True)

        #If the user paid some part in currency, we make the transaction
        if self.currency_amount > 0:
            t = wallet_user.new_transaction(self.currency_amount, wallet=wallet_entity)

        self.status = STATUS_ACCEPTED
        self.save()

    @transaction.atomic
    def cancel_payment(self):

        if self.status != STATUS_PENDING:
            return
            # TODO: create exception

        self.status = STATUS_CANCELLED
        self.save()
