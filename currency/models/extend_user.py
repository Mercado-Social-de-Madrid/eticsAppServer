from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

from currency.models import Entity, Person, PreRegisteredUser


def get_related_entity(self):

    try:
        entity = Entity.objects.filter(user=self).first()
    except Entity.DoesNotExist:
        entity = None
    if entity:
        return ('entity', entity)
    else:
        try:
            person = Person.objects.filter(user=self).first()
        except Person.DoesNotExist:
            person = None
        return ('person', person) if person else ('none', None)

def is_registered(self):
    return not PreRegisteredUser.objects.filter(user=self).exists()

def get_user_by_related(uuid):
    instance = None
    try:
        instance = Entity.objects.get(id=uuid)
    except Entity.DoesNotExist:
        try:
            instance = Person.objects.get(id=uuid)
        except Person.DoesNotExist:
            instance = None
    if not instance:
        raise ObjectDoesNotExist('Sorry, no results on that page.')
    else:
        return instance.user

UserModel = get_user_model()
UserModel.add_to_class("get_related_entity", get_related_entity)
UserModel.add_to_class("is_registered", is_registered)