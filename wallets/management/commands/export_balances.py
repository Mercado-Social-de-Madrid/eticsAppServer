import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q

from currency.models import City
from wallets.models import Wallet


class Command(BaseCommand):
    help = 'Recalculates debit wallet balances'

    def handle(self, *args, **options):

        for wallet in Wallet.objects.all():
            type, instance = wallet.user.get_related_entity() if wallet.user else (None, None)
            if instance:
                if type == 'person':
                    print('{},{},{}'.format(str(instance), instance.nif if instance.nif else '_', wallet.balance))
                else:
                    print('{},{},{}'.format(str(instance), instance.cif if instance.cif else '_', wallet.balance))
