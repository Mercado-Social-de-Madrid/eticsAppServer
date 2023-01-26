from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand

from currency.models import Person, PreRegisteredUser


class Command(BaseCommand):
    help = 'Delete person and asociated user and preregistereduser if exists'

    def add_arguments(self, parser):

        parser.add_argument('person_uuid', type=str, help='Person UUID')



    def handle(self, *args, **options):

        person_uuid = options['person_uuid']
        try:
            person = Person.objects.get(pk=person_uuid)
            print 'Deleting person: {}'.format(person.name)
            try:
                PreRegisteredUser.objects.get(user=person.user).delete()
                print 'Preregistered user deleted'
            except ObjectDoesNotExist:
                print 'Preregistered user does not exist'

            person.user.delete()
            print 'User deleted'
            person.delete()
            print('Person deleted')
        except ObjectDoesNotExist:
            print 'Person does not exist'
