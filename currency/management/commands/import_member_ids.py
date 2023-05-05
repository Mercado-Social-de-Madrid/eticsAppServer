import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from currency.models import Person
from currency.models.category import Category
from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Import member ids data from json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import member ids from')



    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        with open(jsonfile, 'rb') as fp:
            list = json.load(fp)

            for item in list['accounts']:
                member = Person.objects.active().filter(nif=item['cif']).first()
                if not member and item['app_uuid'] and item['app_uuid'] != "None":
                    member = Person.objects.filter(id=item['app_uuid']).first()
                if member is not None:
                    member.member_id = item['member_id']
                    member.save()
                    print("{}: {}".format(item['member_id'], member.display_name))
                else:
                    member = Entity.objects.active().filter(cif=item['cif']).first()
                    if not member and item['app_uuid'] and item['app_uuid'] != "None":
                        member = Entity.objects.filter(id=item['app_uuid']).first()
                    if member is not None:
                        member.member_id = item['member_id']
                        member.save()
                        print("{}: {}".format(item['member_id'], member.display_name))
                    else:
                        print("{} cif not found ({})".format(item['cif'], item['member_id']))


