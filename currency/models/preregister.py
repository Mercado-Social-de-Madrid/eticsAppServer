# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from currency.models import Entity, Person
from helpers import send_template_email


class PreRegisteredUser(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, null=True, blank=True)
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

    print 'aaaa'
    if created:
        user = instance.user
        kind, entity = user.get_related_entity()

        print entity

        send_template_email(
            title='Etics - Registro',
            destination=instance.email,
            template_name='preregister',
            template_params={'token': instance.id, 'entity': entity.display_name}
        )
