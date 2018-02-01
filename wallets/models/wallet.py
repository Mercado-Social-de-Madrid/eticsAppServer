# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from fcm_django.models import FCMDevice


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
    def new_transaction(self, amount, wallet=None, concept=None, bonification=False, is_euro_purchase=False, **kwargs):

        if wallet:
            wallet_from = self
            wallet_to = wallet
        else:
            wallet_from = None
            wallet_to = self

        if not concept:
            if bonification:
                concept = "Bonificación en boniatos por compra"
            elif wallet_from:
                concept = "Transferencia"

        from wallets.models.transaction import Transaction

        transaction = Transaction.objects.create(
            wallet_from=wallet_from,
            wallet_to=wallet_to,
            amount=amount,
            is_bonification=bonification,
            concept=concept,
            is_euro_purchase=is_euro_purchase,
            **kwargs)

        if wallet_from:
            wallet_from.update_balance(transaction)
        wallet_to.update_balance(transaction)

        return transaction


    def update_balance(self, new_transaction):
        self.last_transaction = timezone.now()
        #TODO: calculate balance
        self.save()


    def notify_transaction(self, transaction, silent=False):

        device = FCMDevice.objects.filter(user=self.user).first()
        data = {
            'amount': transaction.amount,
            'is_bonification': transaction.is_bonification,
            'is_euro_purchase': transaction.is_euro_purchase,
            'concept': transaction.concept
        }

        if silent:
            result = device.send_message(data=data)
        else:
            result = device.send_message(title="Has recibido una transferencia", body=data['concept'], data=data)

        print result



# Method to create the wallet for every new user
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        print 'Creating user wallet!'
        Wallet.objects.create(user=instance)

