# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import math

from django.contrib.auth import hashers
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.db import models, transaction
from django.utils import timezone

from helpers import notify_user
from currency.models.extend_user import get_user_by_related
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

    def pending(query, user=None):
        q = query.filter(status=STATUS_PENDING)
        if user is not None:
            q = q.filter(receiver=user)
        return q

    def new_payment(self, sender, receiver_uuid, total_amount=0, currency_amount=0, pin_code=None):

        receiver = get_user_by_related(receiver_uuid)
        if receiver is not None:
            user_type, instance = receiver.get_related_entity()
            status = STATUS_PENDING if user_type == 'entity' else STATUS_ACCEPTED

            if user_type == 'entity':
                # Check that the currency amount is not bigger than the max amount percent
                currency_amount = min(currency_amount, instance.max_accepted_currency(total_amount))

            sender_wallet = Wallet.objects.filter(user=sender).first()

            if sender_wallet.pin_code:
                valid = hashers.check_password(pin_code, sender_wallet.pin_code)
                if not valid:
                    raise PermissionDenied('Wrong ping code')

            if sender_wallet.balance < currency_amount:
                print 'User does not have enough cash!'
                #TODO: Raise exception?

            new_payment = self.create(
                sender=sender,
                receiver=receiver,
                total_amount=total_amount,
                currency_amount=currency_amount,
                status=status)

            new_payment.notify_receiver()
            return new_payment

        else:
            print 'The user doesnt exist!'
            #TODO: Raise exception



class Payment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    processed = models.DateTimeField(auto_now_add=False, null=True, verbose_name='Timestamp procesado')
    sender = models.ForeignKey(User, null=True, related_name='payments_sent')
    receiver = models.ForeignKey(User, null=True, related_name='payments_received')

    status = models.CharField(max_length=10, choices=PAYMENT_STATUS)
    total_amount = models.FloatField(default=0, verbose_name='Importe total')
    currency_amount = models.FloatField(default=0, verbose_name='Cantidad en boniatos')

    objects = PaymentManager()

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['status']

    @transaction.atomic
    def accept_payment(self):

        if self.status != STATUS_PENDING:
            print 'Not pending!'
            return
            #TODO: create exception

        wallet_sender = Wallet.objects.filter(user=self.sender).first()
        wallet_receiver = Wallet.objects.filter(user=self.receiver).first()

        if not wallet_sender or not wallet_receiver:
            print 'Wallet doesnt exist!'
            return
            # TODO: create exception

        #If the user paid some part in currency, we make the transaction
        if self.currency_amount > 0:
            t = wallet_sender.new_transaction(self.currency_amount, wallet=wallet_receiver)
            wallet_receiver.notify_transaction(t, silent=True)

        receiver_type, entity = self.receiver.get_related_entity()
        sender_type, sender = self.sender.get_related_entity()

        if receiver_type == 'entity':
            # If the receiver is an entity, we calculate the bonification to give the sender
            bonus = entity.bonus(self.total_amount, sender_type)
            if bonus > 0:
                t = wallet_receiver.new_transaction(bonus, wallet=wallet_sender, bonus=True)
                print t
                wallet_sender.notify_transaction(t)

        print "Payment accepted"
        self.status = STATUS_ACCEPTED
        self.processed = timezone.now()
        self.save()

    @transaction.atomic
    def cancel_payment(self):

        if self.status != STATUS_PENDING:
            print 'Not pending!'
            return
            # TODO: create exception

        notify_user(user=self.sender, data={}, title="Pago cancelado", message="La entidad ha cancelado el pago")

        print "Payment cancelled"
        self.status = STATUS_CANCELLED
        self.processed = timezone.now()
        self.save()


    def notify_receiver(self, silent=False):

        user_type, sender_instance = self.sender.get_related_entity()
        data = {
            'type': 'payment',
            'amount': self.currency_amount,
            'total_amount': self.total_amount,
            'id': str(self.pk),
            'user_type': user_type,
            'sender': str(sender_instance)
        }

        print 'Notifying payment receiver'
        title = 'Nuevo pago pendiente de confirmar'
        notify_user(self.receiver, title=title, data=data, silent=silent)