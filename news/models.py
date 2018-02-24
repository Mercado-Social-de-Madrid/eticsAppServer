# -*- coding: utf-8 -*-
from __future__ import unicode_literals


import uuid

import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from helpers import RandomFileName


class News(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    published_by = models.ForeignKey(User, null=True)
    title = models.CharField(null=True, blank=True, verbose_name='Título', max_length=250)
    short_description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    banner_image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('news/'),
                                verbose_name='Imagen principal',
                                processors=[ResizeToFit(756, 512, upscale=False)], format='JPEG')
    banner_thumbnail = ImageSpecField(source='banner_image',
                                       processors=[ResizeToFill(400, 200, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    published_date = models.DateTimeField(auto_now_add=True)
    more_info_text = models.CharField(null=True, blank=True, verbose_name='Texto del botón de info', max_length=250)
    more_info_url = models.TextField(null=True, blank=True, verbose_name='URL con más información')


    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-published_date']

    def __unicode__(self):
        return self.title
