import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError


from currency.models import Entity, Person
from wallets.models import Wallet


class Command(BaseCommand):
    help = 'Create a debit transaction'

    def add_arguments(self, parser):
        parser.add_argument('cif', type=str, help='The id for the user')
        parser.add_argument('amount', type=str, help='The amount to add from the debit wallet')


    def handle(self, *args, **options):

        account = options['cif']
        amount = float(options['amount'])

        concept = 'Compra de etics'
        if not amount or not account:
            print 'Wrong arguments'
            return

        try:
            instance = Entity.objects.get(cif=account)
        except Entity.DoesNotExist:
            try:
                instance = Person.objects.get(nif=account)
            except Person.DoesNotExist:
                instance = None

        if not instance:
            print 'No user with that id'
            return

        wallet = instance.user.wallet
        t = Wallet.debit_transaction(wallet=wallet, amount=amount, concept=concept)
