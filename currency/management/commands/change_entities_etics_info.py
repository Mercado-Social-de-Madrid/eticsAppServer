from django.core.management.base import BaseCommand

from currency.models.person import Person
from currency.models.entity import Entity


class Command(BaseCommand):
    help = 'Set automatic 0% etics bonus and 100% etics acceptance for all entities'

    def handle(self, *args, **options):

        entities = Entity.objects.all()

        total = len(entities)
        actual = 0

        for entity in entities:

            actual += 1
            print 'Entity {} of {}'.format(actual, total)

            entity.bonus_percent_entity = 0
            entity.bonus_percent_general = 0
            if entity.max_percent_payment > 0:
                entity.max_percent_payment = 100

            entity.save()

