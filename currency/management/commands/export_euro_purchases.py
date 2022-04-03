import json
import datetime
from django.core.management.base import BaseCommand
from wallets.models.transaction import Transaction
import csv


class Command(BaseCommand):
    help = 'Export list of etics euro purchases'

    def add_arguments(self, parser):

        parser.add_argument('year', type=int, help='Export transactions for this year')

    def handle(self, *args, **options):

        year = options['year']
        start = datetime.datetime(year, 1, 1, 0, 0, 0)
        end = datetime.datetime(year, 12, 31, 23, 59, 59)
        items = Transaction.objects.filter(is_euro_purchase=True, timestamp__range=(start, end))

        print str(len(items)) + " transacciones"

        headers = ['Fecha', 'Hora', 'Nombre y apellidos', 'Nombre usuaria', 'email', 'Cantidad']
        data = []
        for item in items:
            date = item.timestamp.strftime("%d/%m/%Y")
            time = item.timestamp.strftime("%H/%M")
            user = item.wallet_to.user
            full_name = user.first_name.encode('utf-8') + " " + user.last_name.encode('utf-8')
            username = user.username.encode('utf-8')
            email = user.email.encode('utf-8')
            amount = item.amount

            data.append([date, time, full_name, username, email, amount])

        with open('compras_etics.csv', 'w') as f:
            write = csv.writer(f, delimiter=';')
            write.writerow(headers)
            write.writerows(data)

            import os
            absolute_path = os.path.abspath(f)
            print "Guardado en: " + absolute_path

