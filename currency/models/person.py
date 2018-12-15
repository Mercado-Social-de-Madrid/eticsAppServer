# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User, Group
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from helpers import RandomFileName
from currency.models import Entity, City


class Person(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=False, blank=False)
    city = models.ForeignKey(City, null=False, blank=False)

    nif = models.CharField(null=True, blank=True, verbose_name='NIF/CIF', max_length=50)
    email = models.CharField(null=False, blank=False, verbose_name='Email', max_length=250)
    name = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    surname = models.CharField(null=True, blank=True, verbose_name='Apellidos', max_length=250)
    address = models.TextField(null=True, blank=True, verbose_name='Dirección')

    profile_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('profiles/'),
                                verbose_name='Imagen de perfil',
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')
    profile_thumbnail = ImageSpecField(source='profile_image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    registered = models.DateTimeField(auto_now_add=True)
    fav_entities = models.ManyToManyField(Entity, blank=True, verbose_name="Favoritos")

    class Meta:
        verbose_name = 'Persona'
        verbose_name_plural = 'Personas'
        ordering = ['registered']

    @property
    def full_name(self):
        return '{} {}'.format(self.name if self.name else '', self.surname if self.surname else '')

    def __unicode__(self):
        return '{} {}'.format(self.name if self.name else '', self.surname if self.surname else '')

# Method to add every user with a related person to the persons group
@receiver(post_save, sender=Person)
def add_user_to_group(sender, instance, created, **kwargs):

    if created:
        print 'Adding user to persons group'
        group = Group.objects.get(name='persons')
        instance.user.groups.add(group)
