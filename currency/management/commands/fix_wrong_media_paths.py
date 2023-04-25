from django.core.management.base import BaseCommand

from currency.models import Person, Entity


class Command(BaseCommand):
    help = 'Detect wrong media paths starting with /media'

    def handle(self, *args, **options):

        for person in Person.objects.all():
            if person.profile_image and person.profile_image.name.startswith("/media"):
                print(f'{person.name}. {person.profile_image}. (id: {person.id})')
                # remove all /media/ segments at start of path
                parts = person.profile_image.name.split('/')
                if parts[-2] == 'profile':
                    person.profile_image.name = f'{parts[-2]}/{parts[-1]}'
                    person.save()
                else:
                    print(f'Wrong parts: {parts}')

        for entity in Entity.objects.all():
            if entity.logo and entity.logo.name.startswith("/media"):
                print(f'{entity.name}. {entity.logo}. (id: {entity.id})')
                parts = entity.logo.name.split('/')
                if parts[-2] == 'entities':
                    entity.logo.name = f'{parts[-2]}/{parts[-1]}'
                    entity.save()
                else:
                    print(f'Wrong parts: {parts}')

