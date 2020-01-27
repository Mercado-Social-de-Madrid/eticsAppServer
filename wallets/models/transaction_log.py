# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from wallets.models import Wallet, Transaction


class TransactionLogManager(models.Manager):

    def create_log(self, wallet, transaction, new_balance):

        amount = transaction.amount
        instance = None
        name = ''
        if wallet == transaction.wallet_from:
            amount *= -1
            if transaction.wallet_to.user:
                user_type, instance = transaction.wallet_to.user.get_related_entity()
        elif transaction.wallet_from and transaction.wallet_from.user:
            user_type, instance = transaction.wallet_from.user.get_related_entity()

        name = instance.name if instance else None

        return self.create(
            wallet=wallet,
            timestamp=transaction.timestamp,
            amount=amount,
            transaction=transaction,
            related=name,
            concept=transaction.concept,
            made_byadmin=transaction.made_byadmin,
            is_bonification=transaction.is_bonification,
            is_euro_purchase=transaction.is_euro_purchase,
            current_balance=new_balance
        )


class TransactionLog(models.Model):
    wallet = models.ForeignKey(Wallet, blank=True, null=True, related_name='transactions_logs')
    timestamp = models.DateTimeField(verbose_name='Timestamp')
    amount = models.FloatField(default=0, verbose_name='Cantidad')
    concept = models.TextField(blank=True, null=True, verbose_name='Concepto')
    made_byadmin = models.BooleanField(default=False, verbose_name='Realizada por admin')
    is_bonification = models.BooleanField(default=False, verbose_name='Bonificación')
    is_euro_purchase = models.BooleanField(default=False, verbose_name='Compra de euros')
    current_balance = models.FloatField(default=0, verbose_name='Saldo')
    transaction = models.ForeignKey(Transaction, blank=True, null=True)
    related = models.TextField(blank=True, null=True, verbose_name='Concepto')

    objects = TransactionLogManager()

    class Meta:
        verbose_name = 'Movimiento'
        verbose_name_plural = 'Movimientos'
        ordering = ['-timestamp']

