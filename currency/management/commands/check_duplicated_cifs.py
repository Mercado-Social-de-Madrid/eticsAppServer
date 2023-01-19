from django.core.management.base import BaseCommand

from currency.models.person import Person
from currency.models.entity import Entity


class Command(BaseCommand):
    # There was a bug when fetching person info by nif caused by duplicated nif (it was not expected)
    help = 'Detect duplicated person nif or entity cif for debugging (no duplications are expected'

    def handle(self, *args, **options):

        count = 0

        cifs = []
        nifs = []

        for entity in Entity.objects.all():
            if entity.cif in cifs:
                print 'Duplicated entity cif: {}'.format(entity.cif)
            else:
                cifs.append(entity.cif)


        for person in Person.objects.all():
            if person.nif in nifs:
                print 'Duplicated person nif: {}'.format(person.nif)
            else:
                nifs.append(person.nif)

        print '\nFinished. Checked {} cifs and {} nifs'.format(len(cifs), len(nifs))