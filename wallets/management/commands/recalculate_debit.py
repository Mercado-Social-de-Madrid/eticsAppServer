import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db.models import Q

from currency.models import City


class Command(BaseCommand):
    help = 'Recalculates debit wallet balances'

    def handle(self, *args, **options):

        for city in City.objects.all():
            users = User.objects.filter(Q(person__city=city) | Q(entity__city=city))

            balance = 0
            for user in users:
                balance += user.wallet.balance

            print city.full_name
            print balance
            city.wallet.balance = -balance
            city.wallet.save()
