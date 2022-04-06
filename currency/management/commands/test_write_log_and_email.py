import json

from django.core.management.base import BaseCommand

from currency.models.entity import Entity

from django.conf import settings
from django.core.mail import send_mail


def save_log(log, success=False):
    log_file_path = settings.ROOT_DIR + "/log/currency_purchased.txt"
    with open(log_file_path, 'w') as f:
        f.write(log + '\n\n\n')
        f.close()

    send_mail(
        'Nuevo log compra etcs. ' + 'CORRECTO' if success else 'FALLIDO',
        log,
        'Mercado Social <noreply@mercadosocial.net>',
        ['jberzal86@gmail.com'],
    )


class Command(BaseCommand):
    help = 'prueba de log + email'

    def handle(self, *args, **options):
        save_log('esto es una prueba', success=True)


