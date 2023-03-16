# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

import datetime
from django.db import models
from django.db.models import Q
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from helpers import RandomFileName
from currency.models import Entity


class OffersManager(models.Manager):


    def published_last_days(query, days=30):
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        return query.filter(published_date__gte=since)

    def active_last_days(query, days=30):
        today = datetime.date.today()
        since = today - datetime.timedelta(days=days)
        return query.filter(Q(active=True) &
                            (Q(end_date__gte=since) | Q(begin_date__lte=today, begin_date__gte=since) ))

    def current(query, entity=None):
        today = datetime.date.today()
        if entity is None:
            return query.filter(active=True, begin_date__lte=today, end_date__gte=today)
        else:
            return query.filter(active=True, begin_date__lte=today, end_date__gte=today, entity=entity)

    def future(query, entity=None):
        today = datetime.date.today()
        if entity is None:
            return query.filter(Q(begin_date__gt=today) | Q(begin_date__lte=today, end_date__gte=today, active=False))
        else:
            return query.filter(Q(entity=entity) & (Q(begin_date__gt=today) | Q(begin_date__lte=today, end_date__gte=today, active=False)))

    def past(query, entity=None):
        today = datetime.date.today()
        if entity is None:
            return query.filter(end_date__lt=today)
        else:
            return query.filter(end_date__lt=today, entity=entity)

class Offer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.ForeignKey(Entity, null=False, blank=False, related_name='offers', on_delete=models.CASCADE)

    title = models.CharField(null=True, blank=True, verbose_name='Nombre', max_length=250)
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    banner_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('offers/'),
                                verbose_name='Imagen principal',
                                processors=[ResizeToFit(756, 512, upscale=False)], format='JPEG')
    banner_thumbnail = ImageSpecField(source='banner_image',
                                       processors=[ResizeToFill(400, 200, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    published_date = models.DateTimeField(auto_now_add=True)
    discount_percent = models.FloatField(null=True, blank=True, verbose_name='Porcentaje de descuento', default=0)
    discounted_price = models.FloatField(null=True, blank=True, verbose_name='Precio con descuento', default=0)
    active = models.BooleanField(default=True, null=False, verbose_name='Activa')
    begin_date = models.DateField(null=True, blank=True, verbose_name='Fecha de inicio')
    end_date = models.DateField(null=True, blank=True, verbose_name='Fecha de fin')

    objects = OffersManager()

    @property
    def status(self):
        today = datetime.date.today()
        if (self.begin_date > today) or (self.begin_date <= today and self.end_date >= today and self.active == False):
            return 'future'
        elif self.begin_date <= today and self.end_date >= today and self.active:
            return 'current'
        else:
            return 'past'


    class Meta:
        verbose_name = 'Oferta'
        verbose_name_plural = 'Ofertas'
        ordering = ['-published_date']

    def __str__(self):
        return self.title if self.title else self.pk

    def __unicode__(self):
        return self.title if self.title else self.pk
