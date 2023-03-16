# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps
from django.db import models


class City(models.Model):

    id = models.CharField(primary_key=True, max_length=10, null=False, editable=True, verbose_name='Identificador')
    shortname = models.CharField(null=True, blank=True, verbose_name='Nombre corto', max_length=20)
    full_name = models.CharField(null=True, blank=True, verbose_name='Nombre completo', max_length=250)
    latitude = models.FloatField(null=False, verbose_name='Latitud', default=0)
    longitude = models.FloatField(null=False, verbose_name='Longitud', default=0)

    server_base_url = models.CharField(null=False, max_length=250, verbose_name='URL Servidor Gestión', default=0)

    # Debit wallet
    wallet = models.ForeignKey('wallets.wallet', null=True, verbose_name='Monedero de débito', related_name='city_debit', on_delete=models.CASCADE)

    # Social links
    facebook_link = models.CharField(null=True, blank=True, verbose_name='Página de Facebook', max_length=250)
    webpage_link = models.CharField(null=True, blank=True, verbose_name='Página web', max_length=250)
    twitter_link = models.CharField(null=True, blank=True, verbose_name='Perfil de Twitter', max_length=250)
    telegram_link = models.CharField(null=True, blank=True, verbose_name='Canal de Telegram', max_length=250)


    class Meta:
        verbose_name = 'Mercado social'
        verbose_name_plural = 'Mercados sociales'
        ordering = ['id']

    def __unicode__(self):
        return self.shortname if self.shortname else 'MES'

