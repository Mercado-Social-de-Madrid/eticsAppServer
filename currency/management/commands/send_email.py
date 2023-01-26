from django.core.mail import send_mail
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Send email to test it is working'

    def add_arguments(self, parser):

        parser.add_argument('email', type=str, help='Email address')
        parser.add_argument('message', type=str, help='Email message')


    def handle(self, *args, **options):

        email = options['email']
        message = options['message']

        send_mail(
            "Prueba de email por comando (HA)",
            message,
            'TEST Mercado Social <noreply@testmercadosocial.net>',
            [email],
        )
