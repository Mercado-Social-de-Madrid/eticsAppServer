# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth.models import User
from django.db import models

from imagekit.models import ProcessedImageField, ImageSpecField
from pilkit.processors import ResizeToFit, ResizeToFill

from currency.helpers import RandomFileName


class Gallery(models.Model):

    title = models.CharField(null=True, blank=True, verbose_name='Título', max_length=250)
    class Meta:
        verbose_name = 'Galería'
        verbose_name_plural = 'Galerías'

class GalleryPhoto(models.Model):

    gallery = models.ForeignKey(Gallery, null=True, related_name='photos')
    order = models.IntegerField(verbose_name='Orden', default=0)
    title = models.CharField(null=True, blank=True, verbose_name='Título', max_length=250)
    image = ProcessedImageField(null=True, blank=True, upload_to=RandomFileName('photos/'),
                                processors=[ResizeToFit(512, 512, upscale=False)], format='JPEG')

    image_thumbnail = ImageSpecField(source='image',
                                       processors=[ResizeToFill(150, 150, upscale=False)],
                                       format='JPEG',
                                       options={'quality': 70})

    uploaded = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Foto'
        verbose_name_plural = 'Fotos'
        ordering = ['order']
