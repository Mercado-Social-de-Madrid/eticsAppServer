import json

from django.core.management.base import BaseCommand

from currency.models import Person


class Command(BaseCommand):
    help = 'Export consumers to a json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to export consumers')

    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        items = Person.objects.all()

        data = []
        for item in items:

            data.append({
                'id': str(item.id),
                'nif': item.nif,
                'name': item.name,
                'surname': item.surname,
                'email': item.email,
                'address': item.address,
                'member_id': item.member_id,
                'profile_image': item.profile_image.name,
                'profile_thumbnail': item.profile_thumbnail.name,
                'registered': str(item.registered),
                'is_intercoop': item.is_intercoop,
                'inactive': item.inactive,
                'fav_entities': list(map(lambda entity: str(entity.id), item.fav_entities.all())),
            })

        with open(jsonfile, 'w') as f:
            json_entities = json.dumps(data)
            f.write(json_entities)
            f.close()

