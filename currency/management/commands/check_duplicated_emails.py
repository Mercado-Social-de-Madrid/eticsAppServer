from django.core.management.base import BaseCommand

from currency.models.person import Person
from currency.models.entity import Entity


class Command(BaseCommand):
    # There was a bug when fetching person info by nif caused by duplicated nif (it was not expected)
    help = 'Detect duplicated person nif or entity cif for debugging (no duplications are expected'

    def handle(self, *args, **options):

        count = 0

        emails = []

        for entity in Entity.objects.active():
            if entity.email in emails:
                print('Duplicated entity cif: {}. Email: {}'.format(entity.cif, entity.email))
            else:
                emails.append(entity.cif)

        for person in Person.objects.active():
            if person.email in emails:
                print('Duplicated person nif: {}. Email: {}'.format(person.nif, person.email))
            else:
                emails.append(person.nif)

        print('\nFinished. Checked {} emails'.format(len(emails)))