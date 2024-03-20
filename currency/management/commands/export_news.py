import json

from django.core.management.base import BaseCommand

from news.models import News


class Command(BaseCommand):
    help = 'Export categories to a json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to export categories')

    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        items = News.objects.all()

        data = []
        for item in items:

            data.append({
                'id': str(item.id),
                'title': item.title,
                'description': item.description,
                'short_description': item.short_description,
                'banner_image': item.banner_image.name,
                'banner_thumbnail': item.banner_thumbnail.name,
                'published_date': str(item.published_date),
                'more_info_text': item.more_info_text,
                'more_info_url': item.more_info_url,

            })

        with open(jsonfile, 'w') as f:
            json_entities = json.dumps(data)
            f.write(json_entities)
            f.close()

