import codecs

import requests
import sys
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from currency.models import City, Person, Entity


class Command(BaseCommand):
    help = 'Update user emails based on their entity/person'

    def handle(self, *args, **options):

        for person in Person.objects.all():
            if person.user and person.email != person.user.email:
                line = u'{}: Different email!'.format(person.display_name)
                print(line)
                person.user.email = person.email
                person.user.save()

        for entity in Entity.objects.all():
            if entity.user and entity.email != entity.user.email:
                line = u'{}: Different email!'.format(entity.display_name)
                print(line)
                entity.user.email = entity.email
                entity.user.save()

        print 'All up-to-date.'
