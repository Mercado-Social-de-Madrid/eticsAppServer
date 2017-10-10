from django.contrib.auth import get_user_model

from currency.models import Entity, Person


def get_related_entity(self):

    try:
        entity = Entity.objects.get(user=self)
    except Entity.DoesNotExist:
        entity = None
    if entity:
        return ('entity', entity)
    else:
        try:
            person = Person.objects.get(user=self)
        except Person.DoesNotExist:
            person = None

        return ('person', person) if person else ('none', None)

UserModel = get_user_model()
UserModel.add_to_class("get_related_entity", get_related_entity)