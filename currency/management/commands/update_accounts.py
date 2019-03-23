import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from currency.models import City


class Command(BaseCommand):
    help = 'Fetch current status of every user in the system from the external source'

    def add_arguments(self, parser):

        # Optional argument to start the summary calculation from the beginning
        parser.add_argument(
            '--fromstart',
            action='store_true',
            dest='fromstart',
            help='Calculate summary tables from the beginning, not just the last ones',
        )

    def compose_url(self, base_url, account_pk, is_guest=False):
        return ('{}api/v1/' + ('guest' if is_guest else 'account') + '/{}').format(base_url, account_pk)

    def handle(self, *args, **options):
        users = User.objects.filter(wallet__isnull=False).distinct()
        for user in users:

            account_pk = None
            is_guest = False
            type, account = user.get_related_entity()
            if type == 'entity':
                account_pk = account.cif
            elif type == 'person':
                account_pk = account.nif
                is_guest = account.is_guest_account

            if not account_pk:
                continue

            if account.city.server_base_url:

                api_url = self.compose_url(account.city.server_base_url, account_pk, is_guest)
                try:
                    r = requests.get(api_url)

                    if r.ok:
                        body = r.json()
                        user.is_active = body['is_active']
                        user.save()

                        if is_guest:
                            account.expiration_date = body['expiration_date']
                            account.save()
                        print unicode('User {} updated!').format(account)
                    else:
                        print unicode('User {} not found!').format(account)

                except Exception as e:
                    pass

        #if options['fromstart']:
