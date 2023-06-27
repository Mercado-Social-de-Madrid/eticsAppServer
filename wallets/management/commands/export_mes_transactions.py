import csv
from django.core.management.base import BaseCommand
from wallets.models import Wallet, TransactionLog


class Command(BaseCommand):
    help = 'Export transactions of MES'

    def handle(self, *args, **options):

        wallet = Wallet.objects.get(pk='073bcade-b3a6-495e-a835-f6eab3d66134')
        transactions = TransactionLog.objects.filter(wallet=wallet)
        print(len(transactions))

        headers = ['Fecha', 'Hora', 'Cuenta', 'Concepto', 'Cantidad', 'Saldo']
        data = []
        for item in transactions:
            date = item.timestamp.strftime("%d/%m/%Y")
            time = item.timestamp.strftime("%H/%M")
            account = item.related
            concept = item.concept
            amount = item.amount
            balance = item.current_balance

            data.append([date, time, account, concept, amount, balance])

        with open('transactions_mes.csv', 'w') as f:
            write = csv.writer(f, delimiter=';')
            write.writerow(headers)
            write.writerows(data)
