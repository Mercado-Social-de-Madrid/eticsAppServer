import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from currency.models.category import Category
from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Import entity profile data from json file'

    def add_arguments(self, parser):

        parser.add_argument('jsonfile', type=str, help='Indicates the JSON file to import entities from')



    def handle(self, *args, **options):

        jsonfile = options['jsonfile']

        entities = []
        with open(jsonfile, 'rb') as fp:
            list = json.load(fp)

            for item in list:

                try:
                    entity = Entity.objects.get(email=item['email'])
                except:
                    continue

                if 'name' in item and item['name']:
                    entity.name = item['name']

                if 'email' in item and item['email']:
                    entity.email = item['email']

                if 'address' in item and item['address']:
                    entity.address = item['address']

                if 'description' in item and item['description']:
                    entity.description = item['description']

                if 'short_description' in item and item['short_description']:
                    entity.short_description = item['short_description']

                if 'latitude' in item and item['latitude']:
                    entity.latitude = item['latitude']

                if 'longitude' in item and item['longitude']:
                    entity.longitude = item['longitude']

                if 'max_percent_payment' in item and item['max_percent_payment']:
                    entity.max_percent_payment = item['max_percent_payment']

                if 'bonus_percent_general' in item and item['bonus_percent_general']:
                    entity.bonus_percent_general = item['bonus_percent_general']

                if 'bonus_percent_entity' in item and item['bonus_percent_entity']:
                    entity.bonus_percent_entity = item['bonus_percent_entity']

                if 'facebook_link' in item and item['facebook_link']:
                    entity.facebook_link = item['facebook_link']

                if 'twitter_link' in item and item['twitter_link']:
                    entity.twitter_link = item['twitter_link']

                if 'instagram_link' in item and item['instagram_link']:
                    entity.instagram_link = item['instagram_link']

                if 'telegram_link' in item and item['telegram_link']:
                    entity.telegram_link = item['telegram_link']

                if 'webpage_link' in item and item['webpage_link']:
                    entity.webpage_link = item['webpage_link']

                entity.categories.clear()
                print(entity.name)
                for categ_name in item['categories']:
                    category = Category.objects.get(name=categ_name)
                    if not category:
                        raise Exception('category not found: ' + categ_name + ", Entity: " + entity.name)
                    entity.categories.add(category)

                entities.append(entity)

            print('Saving entities lenght: ' + str(len(entities)))
            for entity in entities:

                print('saving: ' + entity.name)
                try:
                    entity.save()
                except IntegrityError as e:
                    print(e)
                except Exception as e:
                    print(e)
