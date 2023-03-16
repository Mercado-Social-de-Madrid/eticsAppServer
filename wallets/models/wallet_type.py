# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid

from django.contrib.auth import hashers
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from helpers import notify_user


class WalletType(models.Model):

    id = models.CharField(primary_key=True, max_length=25, null=False, editable=False)
    name = models.CharField(max_length=150, null=False, editable=False, verbose_name='Nombre')
    description = models.TextField(null=True, blank=True, verbose_name='Descripción')
    credit_limit = models.FloatField(null=False, default=0, verbose_name='Límite de crédito')
    unlimited = models.BooleanField(default=False, verbose_name='Crédito ilimitado')

    class Meta:
        verbose_name = 'Tipo de cuenta'
        verbose_name_plural = 'Tipos de cuenta'
        ordering = ['id']

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


