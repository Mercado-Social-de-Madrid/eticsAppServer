# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import datetime
from django.db import models
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from currency.helpers import RandomFileName
from currency.models import Entity


class OffersManager(models.Manager):

    def current(query):
        today = datetime.date.today()
        return query.filter(active=True, begin_date__lte=today, end_date__gte=today)


class Offer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, null=False, blank=False, related_name='offers')

    title = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    banner_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('offers/'),
                                verbose_name='Imagen principal',
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')
    banner_thumbnail = ImageSpecField(source='banner_image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    published_date = models.DateTimeField(auto_now_add=True)
    discount_percent = models.FloatField(null=True, blank=True, verbose_name='Porcentaje de descuento', default=0)
    discounted_price = models.FloatField(null=True, blank=True, verbose_name='Precio con descuento', default=0)
    active = models.BooleanField(null=False, verbose_name='Activa')
    begin_date = models.DateField(null=True, blank=True, verbose_name='Fecha de inicio')
    end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin')

    objects = OffersManager()

    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
        ordering = ['-published_date']

    def __unicode__(self):
        return self.title
