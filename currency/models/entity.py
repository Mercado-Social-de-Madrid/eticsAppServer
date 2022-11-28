# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import math

from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.urls import reverse

from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

import helpers
from helpers import RandomFileName
from currency.models import Category, Gallery, City



class EntityManager(models.Manager):

    def active(query):
        return query.filter(inactive=False, hidden=False)


class Entity(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, null=False, blank=False)
    city = models.ForeignKey(City, null=False, blank=False)

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
    bonus_percent_entity = models.FloatField(default=0, verbose_name='Porcentaje de bonificación a entidades', validators = [MinValueValidator(0), MaxValueValidator(100)])
    bonus_percent_general = models.FloatField(default=0, verbose_name='Porcentaje de bonificación general', validators = [MinValueValidator(0), MaxValueValidator(100)])
    max_percent_payment = models.FloatField(default=0, verbose_name='Máximo porcentaje de pago aceptado', validators = [MinValueValidator(0), MaxValueValidator(100)])
    num_workers = models.IntegerField(default=0, verbose_name='Número de trabajadores', validators = [MinValueValidator(0)])
    legal_form = models.TextField(null=True, blank=True, verbose_name='Formulario legal')

    # Social links
    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    telegram_link = models.CharField(null=True, blank=True, verbose_name='Canal de Telegram', max_length=250)
    instagram_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Instagram', max_length=250)

    inactive = models.BooleanField(default=False, verbose_name='Inactiva')
    hidden = models.BooleanField(default=False, verbose_name='Oculta')

    gallery = models.OneToOneField(Gallery, blank=True, null=True, on_delete=models.SET_NULL)

    objects = EntityManager()

    @property
    def display_name(self):
        return self.name

    @property
    def first_photo_url(self):
        if self.gallery and self.gallery.photos.count() > 0:
            image = self.gallery.photos.all().first()
            if image:
                return image.image.url
        return None

    @property
    def qr_code(self):
        return settings.BASESITE_URL + reverse('entity_qr_detail',  kwargs={'pk': self.pk} )

    def bonus(self, total_amount, bonusable_type=None):
        percent = self.bonus_percent_general
        if bonusable_type == 'entity':
            percent = self.bonus_percent_entity

        return round(total_amount * (percent / 100.0), 2)

    def max_accepted_currency(self, total_amount):
        return round(total_amount * (self.max_percent_payment / 100.0), 2)

    class Meta:
        verbose_name = 'Entidad'
        verbose_name_plural = 'Entidades'
        ordering = ['name']

    def __unicode__(self):
        return self.name if self.name else 'Entidad'




# Method to add every user with a related entity to the entities group
@receiver(post_save, sender=Entity)
def add_user_to_group(sender, instance, created, **kwargs):

    if instance.user:
        instance.user.email = instance.email
        instance.user.save()

    if created:
        print 'Adding user to entities group'
        group = Group.objects.get(name='entities')
        instance.user.groups.add(group)

        if not instance.gallery:
            instance.gallery = Gallery.objects.create()


    """
        helpers.mailing.send_template_email(
            'Bienvenid@ a la app del Mercado social',
            instance.email,
            'welcome_entity',
            { 'entity': instance }
        )
    """


@receiver(pre_save, sender=Entity)
def check_links(sender, instance, **kwargs):

    if instance.facebook_link and not instance.facebook_link.startswith('http'):
        if not instance.facebook_link.startswith("https://facebook.com/"):
            instance.facebook_link = "https://www.facebook.com/" + instance.facebook_link.replace("@", "").strip()
        else:
            instance.facebook_link = "https://" + instance.facebook_link

    if instance.webpage_link and not instance.webpage_link.startswith('http'):
        instance.webpage_link = "http://" + instance.webpage_link.strip()

    if instance.twitter_link and not instance.twitter_link.startswith('http'):
        if not instance.twitter_link.startswith("https://twitter.com/"):
            instance.twitter_link = "https://twitter.com/" + instance.twitter_link.replace("@", "").strip()
        else:
            instance.twitter_link = "https://" + instance.twitter_link

    if instance.telegram_link and not instance.telegram_link.startswith('http'):
        if not instance.telegram_link.startswith("https://telegram.me/"):
            instance.telegram_link = "https://telegram.me/" + instance.telegram_link.replace("@", "").strip()
        else:
            instance.telegram_link = "https://" + instance.telegram_link

    if instance.instagram_link and not instance.instagram_link.startswith('http'):
        if not instance.instagram_link.startswith("https://instagram.com/"):
            instance.instagram_link = "https://instagram.com/" + instance.instagram_link.replace("@", "").strip()
        else:
            instance.instagram_link = "https://" + instance.instagram_link