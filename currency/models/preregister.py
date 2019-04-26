# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from currency.models import Entity, Person
from helpers import send_template_email


class PreRegisteredUser(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True, related_name='preregister')
    entity = models.ForeignKey(Entity, verbose_name='Entidad', null=True)
    person = models.ForeignKey(Person, verbose_name='Consumidora', null=True)
    email = models.EmailField(blank=True)

    class Meta:
        verbose_name = 'Prerregistro'
        verbose_name_plural = 'Prerregistros'
        ordering = ['email']

    def __unicode__(self):
        return self.email if self.email else ''


# Method to add every user with a related entity to the entities group
@receiver(post_save, sender=PreRegisteredUser)
def send_welcome_email(sender, instance, created, **kwargs):

    if created:
        user = instance.user
        kind, entity = user.get_related_entity()

        template = 'preregister_entity'
        template = 'preregister_entity' if kind == 'entity' else 'preregister_person'
        if kind == 'person' and entity.is_guest_account and settings.SPECIAL_WELCOME:
            template = 'preregister_special'

        title = 'Todo listo para que tu entidad aparezca en la aplicación móvil del Mercado Social' if kind == 'entity' else 'Todo listo para empezar a usar la aplicación móvil del Mercado Social'

        send_template_email(
            title=title,
            destination=instance.email,
            template_name=template,
            template_params={'token': instance.id, 'entity': entity.display_name}
        )
