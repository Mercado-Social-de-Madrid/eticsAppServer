from django.core.management.base import BaseCommand

from currency.models.person import Person
from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Generate correlative member ids for local test servers'

    def handle(self, *args, **options):

        number = 1
        for person in Person.objects.all():
            id = "{:06d}".format(number)
            person.member_id = id
            person.save()
            number += 1
            print(id)

        for entity in Entity.objects.all():
            id = "{:06d}".format(number)
            entity.member_id = id
            entity.save()
            number += 1
            print(id)

