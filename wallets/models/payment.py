# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import datetime
from django.contrib.auth import hashers
from django.contrib.auth.models import User
from django.db import models, transaction
from django.utils import timezone

from currency.models.extend_user import get_user_by_related
from helpers import notify_user
from wallets.models import Wallet

STATUS_ACCEPTED = 'accepted'
STATUS_CANCELLED = 'cancelled'
STATUS_PENDING = 'pending'
PAYMENT_STATUS = (
    (STATUS_ACCEPTED, 'Aceptado'),
    (STATUS_CANCELLED, 'Cancelado'),
    (STATUS_PENDING, 'Pendiente'),
)


class PaymentQuerySet(models.QuerySet):
    def pending(self, user=None):
        q = self.filter(status=STATUS_PENDING)
        if user is not None:
            q = q.filter(receiver=user)
        return q

    def sent_pending(self, user):
        return self.filter(status=STATUS_PENDING, sender=user)


    def published_last_days(self, days=30):
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        return self.filter(timestamp__gte=since)

class PaymentManager(models.Manager):

    def get_queryset(self):
        return PaymentQuerySet(self.model, using=self._db)  # Important!

    def pending(self, user=None):
        return self.get_queryset().pending(user=user)

    def sent_pending(self, user=None):
        return self.get_queryset().sent_pending(user=user)

    def published_last_days(self, days=30):
        return self.get_queryset().published_last_days(days=days)

    def new_payment(self, sender, receiver_uuid, total_amount=0, currency_amount=0, concept=None, pin_code=None):

        receiver = get_user_by_related(receiver_uuid)

        receiver_type, entity = receiver.get_related_entity()
        sender_type, sender_entity = sender.get_related_entity()

        if entity.city != sender_entity.city:
            raise Exception('Different cities!')

        if sender_type == 'person' and sender_entity.is_guest_account:
            if sender_entity.expiration_date < datetime.date.today():
                raise Wallet.GuestExpired

        if receiver is not None:
            status = STATUS_PENDING if receiver_type == 'entity' else STATUS_ACCEPTED

            if receiver_type == 'entity':
                # Check that the currency amount is not bigger than the max amount percent
                currency_amount = min(currency_amount, entity.max_accepted_currency(total_amount))

                if not entity.user.is_registered():
                    raise Wallet.ReceiverNotRegistered

            sender_wallet = Wallet.objects.filter(user=sender).first()

            if sender_wallet.pin_code:
                valid = hashers.check_password(pin_code, sender_wallet.pin_code)
                if not valid:
                    raise Wallet.WrongPinCode

            if not sender_wallet.has_enough_balance(currency_amount):
                raise Wallet.NotEnoughBalance(sender_wallet)

            new_payment = self.create(
                sender=sender,
                receiver=receiver,
                total_amount=total_amount,
                concept=concept,
                currency_amount=currency_amount,
                status=status)

            new_payment.notify_receiver()
            return new_payment

        else:
            raise Exception('The user doesnt exist')



class Payment(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Timestamp')
    processed = models.DateTimeField(auto_now_add=False, null=True, verbose_name='Timestamp procesado')
    sender = models.ForeignKey(User, null=True, related_name='payments_sent', on_delete=models.SET_NULL)
    receiver = models.ForeignKey(User, null=True, related_name='payments_received', on_delete=models.SET_NULL)
    concept = models.TextField(null=True, blank=True, verbose_name='Concepto (opcional)')

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
            return
            #TODO: create exception

        wallet_sender = Wallet.objects.filter(user=self.sender).first()
        wallet_receiver = Wallet.objects.filter(user=self.receiver).first()

        if not wallet_sender or not wallet_receiver:
            return
            # TODO: create exception

        receiver_type, entity = self.receiver.get_related_entity()
        sender_type, sender = self.sender.get_related_entity()

        #If the user paid some part in currency, we make the transaction
        if self.currency_amount > 0:
            t = wallet_sender.new_transaction(self.currency_amount, wallet=wallet_receiver, from_payment=self, concept=self.concept)
            wallet_receiver.notify_transaction(t, silent=True)

        if receiver_type == 'entity':
            # If the receiver is an entity, we calculate the bonification to give the sender
            bonus = entity.bonus(self.total_amount, sender_type)
            if bonus > 0:
                t = wallet_receiver.new_transaction(bonus, wallet=wallet_sender, bonus=True, concept=self.concept)
                wallet_sender.notify_transaction(t)

        self.status = STATUS_ACCEPTED
        self.processed = timezone.now()
        self.save()

    @transaction.atomic
    def cancel_payment(self):

        if self.status != STATUS_PENDING:
            return
            # TODO: create exception

        notify_user(user=self.sender, data={}, title="Pago cancelado", message="La entidad ha cancelado el pago")

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

        title = 'Nuevo pago pendiente de confirmar'
        notify_user(self.receiver, title=title, data=data, silent=silent)