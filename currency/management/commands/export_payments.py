
from django.core.management.base import BaseCommand
from wallets.models.payment import Payment
import csv


class Command(BaseCommand):
    help = 'Export list of payments'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        items = Payment.objects.all()

        print "pagos totales: " + str(len(items))
        print "pagos con etics: " + str(len(Payment.objects.filter(currency_amount__gt=0)))

        headers = ['Fecha', 'Hora', 'Pagador', 'Destinatario', 'Estado', 'Cantidad total', 'En etics']
        data = []
        for item in items:
            date = item.timestamp.strftime("%d/%m/%Y")
            time = item.timestamp.strftime("%H/%M")
            sender = item.sender.username.encode('utf-8')
            receiver = item.receiver.username.encode('utf-8')

            # full_name = user.first_name.encode('utf-8') + " " + user.last_name.encode('utf-8')
            # username = user.username.encode('utf-8')
            # email = user.email.encode('utf-8')

            status = item.status.encode('utf-8')
            total_amount = item.total_amount
            currency_amount = item.currency_amount

            data.append([date, time, sender, receiver, status, total_amount, currency_amount])

        with open('pagos.csv', 'w') as f:
            write = csv.writer(f, delimiter=';')
            write.writerow(headers)
            write.writerows(data)


