import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from currency.models import Person
from currency.models.category import Category
from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Import balance reports for providers from json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import data from')



    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        media_path = 'https://gestionmadrid.mercadosocial.net/media/'

        with open(jsonfile, 'rb') as fp:
            list = json.load(fp)

            for item in list:
                member = Entity.objects.filter(cif=item['cif']).first()
                if not member:
                    member = Entity.objects.filter(member_id=item['member_id']).first()
                if member is not None:
                    balance_report = item['balance_report']
                    if balance_report:
                        if not balance_report.startswith('reports'):
                            balance_report = "reports/" + balance_report

                        balance_detail = media_path + balance_report
                        member.balance_detail = balance_detail
                        member.save()
                    print("{}: {}".format(item['member_id'], member.display_name))
                else:
                    print("{} cif not found ({})".format(item['cif'], item['member_id']))


