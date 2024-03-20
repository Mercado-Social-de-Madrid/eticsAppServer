import json

from django.core.management.base import BaseCommand

from currency.models import Category


class Command(BaseCommand):
    help = 'Export categories to a json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to export categories')

    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        items = Category.objects.all()

        data = []
        for item in items:

            data.append({
                'id': str(item.id),
                'name': item.name,
                'description': item.description,
                'color': item.color,
            })

        with open(jsonfile, 'w') as f:
            json_entities = json.dumps(data)
            f.write(json_entities)
            f.close()

