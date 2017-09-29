from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

from currency.models import Entity


def get_related_entity(self):

    try:
        entity = Entity.objects.get(user=self)
    except Entity.DoesNotExist:
        entity = None

    if entity:
        return ('entity', entity)
    else:
        return ('none', None)

UserModel = get_user_model()
UserModel.add_to_class("get_related_entity", get_related_entity)