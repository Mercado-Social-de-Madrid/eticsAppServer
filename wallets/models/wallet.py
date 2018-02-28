# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpers import notify_user


class Wallet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User)
    balance = models.FloatField(default=0, verbose_name='Saldo actual')
    last_transaction = models.DateTimeField(blank=True, null=True, verbose_name='Última transacción')

    class Meta:
        verbose_name = 'Monedero'
        verbose_name_plural = 'Monederos'
        ordering = ['user']

    def __unicode__(self):
        return self.user.username + ': ' + str(self.balance)


    @transaction.atomic
    def new_transaction(self, amount, wallet=None, concept=None, bonus=False, is_euro_purchase=False, **kwargs):

        if wallet:
            wallet_from = self
            wallet_to = wallet
        else:
            wallet_from = None
            wallet_to = self

        if not concept:
            if bonus:
                concept = "Bonificación en boniatos por compra"
            elif wallet_from:
                concept = "Transferencia"

        from wallets.models.transaction import Transaction

        transaction = Transaction.objects.create(
            wallet_from=wallet_from,
            wallet_to=wallet_to,
            amount=amount,
            is_bonification=bonus,
            concept=concept,
            is_euro_purchase=is_euro_purchase,
            **kwargs)

        if wallet_from:
            wallet_from.update_balance(transaction, is_sender=True)
        wallet_to.update_balance(transaction, is_receiver=True)

        return transaction

    @transaction.atomic
    def update_balance(self, new_transaction, is_sender=False, is_receiver=False):
        self.last_transaction = new_transaction.timestamp

        if is_sender:
            self.balance -= new_transaction.amount
        if is_receiver:
            self.balance += new_transaction.amount

        from wallets.models import TransactionLog
        TransactionLog.objects.create_log(self, new_transaction, self.balance)

        self.save()


    def notify_transaction(self, transaction, silent=False):

        data = {
            'type': 'transaction',
            'amount': transaction.amount,
            'is_bonification': transaction.is_bonification,
            'is_euro_purchase': transaction.is_euro_purchase,
            'concept': transaction.concept
        }

        title = 'Ya tienes tu bonificación!' if transaction.is_bonification else 'Has recibido una transferencia'
        notify_user(self.user, title=title, message=data['concept'], data=data, silent=silent)


# Method to create the wallet for every new user
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        print 'Creating user wallet!'
        Wallet.objects.create(user=instance)

