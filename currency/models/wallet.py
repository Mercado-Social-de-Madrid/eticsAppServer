# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


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


# Method to create the wallet for every new user
@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        print 'Creating user wallet!'
        Wallet.objects.create(user=instance)


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
    wallet_from = models.ForeignKey(Wallet, blank=True, null=True, related_name='transactions_from')
    wallet_to = models.ForeignKey(Wallet, related_name='transactions_to')
    amount = models.FloatField(default=0, verbose_name='Cantidad')
    concept = models.TextField(blank=True, null=True, verbose_name='Concepto')
    timestamp = models.DateTimeField(blank=True, null=True, verbose_name='Última transacción')
    status = models.CharField(default=STATUS_PENDING, max_length=20, choices=TRANSACTION_STATUS, verbose_name='Estado')

    tax_processed = models.BooleanField(default=False, verbose_name='Impuestos procesados')
    made_byadmin = models.BooleanField(default=False, verbose_name='Realizada por admin')
    is_bonification = models.BooleanField(default=False, verbose_name='Bonificación')
    is_euro_purchase = models.BooleanField(default=False, verbose_name='Compra de euros')

    rel_transaction = models.ForeignKey('self', null=True, blank=True)
    comments = models.TextField(null=True, blank=True, verbose_name='Comentarios adicionales')
