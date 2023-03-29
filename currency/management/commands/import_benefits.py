import csv
from io import TextIOWrapper

from django.core.management import BaseCommand

from benefits.models import Benefit
from currency.models import Entity


class Command(BaseCommand):
    help = 'Import benefits data from csv file'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import benefits from')

    def handle(self, *args, **options):

        csvfile = options['csvfile']

        benefits = []
        with open(csvfile, 'rb') as file:
            list = csv.DictReader(TextIOWrapper(file, newline="", encoding="utf-8"))
            for item in list:
                benefit = Benefit()
                try:
                    benefit.entity = Entity.objects.get(cif=item['cif'])
                    benefit.in_person = 'TRUE' == item['in_person']
                    benefit.online = 'TRUE' == item['online']
                    benefit.includes_intercoop_members = 'TRUE' == item['not_for_intercoop_socias']
                    benefit.benefit_for_entities = item['% Descuento Entidades']
                    benefit.benefit_for_members = item['% Descuento Consumidoras']
                    benefit.discount_code = item['Código de descuento']
                    benefit.discount_link_entities = item['Link entidades']
                    benefit.discount_link_members = item['Link consumidoras']
                    benefit.save()
                except Entity.DoesNotExist:
                    print("Entity with cif: " + item['cif'] + " and name: " + item['Nombre entidad'] + ' does not exist')