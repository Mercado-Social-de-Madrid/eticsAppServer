# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth import hashers
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from currency.models import Entity
from currency.models.extend_user import get_related_entity
from helpers import notify_user
from wallets.models import WalletType


class Wallet(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User)
    type = models.ForeignKey(WalletType, null=True, related_name='wallets')
    balance = models.FloatField(default=0, verbose_name='Saldo actual')
    last_transaction = models.DateTimeField(blank=True, null=True, verbose_name='Última transacción')
    pin_code = models.CharField(null=True, max_length=100, verbose_name='Código PIN (hasheado)')


    class Meta:
        verbose_name = 'Monedero'
        verbose_name_plural = 'Monederos'
        ordering = ['user']

    def __unicode__(self):
        return self.user.username + ': ' + str(self.balance)

    def set_type(self, type='default'):
        if not type:
            type = 'default'
        try:
            wallet_type = WalletType.objects.get(id=type)
        except WalletType.DoesNotExist:
            wallet_type = None

        if wallet_type:
            self.type = wallet_type
            self.save()


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


    def update_pin_code(self, pin_code):
        self.pin_code = hashers.make_password(pin_code)
        self.save()

    @staticmethod
    def update_user_pin_code(user, pin_code):
        wallet = Wallet.objects.filter(user=user).first()
        if wallet:
            wallet.update_pin_code(pin_code)


# Method to create the wallet for every new user
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        print 'Creating user wallet!'
        wallet, new = Wallet.objects.get_or_create(user=instance)

        type, related = instance.get_related_entity()
        print type
        wallet_type = 'entity' if type == 'entity' else 'default'
        wallet.set_type(wallet_type)

        if not new:
            print 'Wallet for user already existed'


# Method to generate the entity wallet type
@receiver(post_save, sender=Entity)
def add_user_to_group(sender, instance, created, **kwargs):

    if created:
        wallet, new = Wallet.objects.get_or_create(user=instance.user)
        wallet.set_type('entity')
