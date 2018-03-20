# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

import helpers
from helpers import RandomFileName
from currency.models import Category, Gallery


class Entity(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=False, blank=False)
    cif = models.CharField(null=True, blank=True, verbose_name='NIF/CIF', max_length=50)
    email = models.CharField(null=False, blank=False, verbose_name='Email', max_length=250)
    name = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    short_description = models.TextField(null=True, blank=True, verbose_name='Descripción corta')
    phone_number = models.CharField(null=True, blank=True, verbose_name='Teléfono', max_length=25)
    address = models.TextField(null=True, blank=True, verbose_name='Dirección')

    logo = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('entities/'),
                                verbose_name='Imagen de perfil',
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')
    logo_thumbnail = ImageSpecField(source='logo',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    registered = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField(null=False, verbose_name='Latitud', default=0)
    longitude = models.FloatField(null=False, verbose_name='Longitud', default=0)

    categories = models.ManyToManyField(Category, blank=True, verbose_name='Categorías')

    # Currency fields
    bonus_percent_entity = models.FloatField(default=0, verbose_name='Porcentaje de bonificación a entidades')
    bonus_percent_general = models.FloatField(default=0, verbose_name='Porcentaje de bonificación general')
    max_percent_payment = models.FloatField(default=0, verbose_name='Máximo porcentaje de pago aceptado')
    num_workers = models.IntegerField(default=0, verbose_name='Número de trabajadores')
    legal_form = models.TextField(null=True, blank=True, verbose_name='Formulario legal')

    # Social links
    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    telegram_link = models.CharField(null=True, blank=True, verbose_name='Canal de Telegram', max_length=250)
    instagram_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Instagram', max_length=250)

    gallery = models.OneToOneField(Gallery, blank=True, null=True, on_delete=models.SET_NULL)

    @property
    def first_photo_url(self):
        if self.gallery and self.gallery.photos.count() > 0:
            image = self.gallery.photos.all().first()
            if image:
                return image.image.url
        return None

    def bonus(self, total_amount, bonusable_type=None):
        percent = self.bonus_percent_general
        if bonusable_type == 'entity':
            percent = self.bonus_percent_entity

        return total_amount * (percent / 100.0)

    def max_accepted_currency(self, total_amount):
        return total_amount * (self.max_percent_payment / 100.0)

    class Meta:
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'
        ordering = ['registered']

    def __unicode__(self):
        return self.name


# Method to add every user with a related entity to the entities group
@receiver(post_save, sender=Entity)
def add_user_to_group(sender, instance, created, **kwargs):

    if created:
        print 'Adding user to entities group'
        group = Group.objects.get(name='entities')
        instance.user.groups.add(group)

        if not instance.gallery:
            instance.gallery = Gallery.objects.create()

        helpers.mailing.send_template_email(
            'Bienvenid@ a la app del Mercado social',
            instance.email,
            'welcome_entity',
            { 'entity': instance }
        )
