# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-12-17 13:04
from __future__ import unicode_literals

from django.db import migrations

def create_initial_city(apps, schema_editor):
    # We can't import the model directly as it may be a newer
    # version than this migration expects. We use the historical version.
    Wallet = apps.get_model('wallets', 'wallet')
    City = apps.get_model('currency', 'city')

    city = City.objects.create(
        id='mad',
        shortname='Madrid',
        full_name='Mercado Social de Madrid',
        latitude= 40.416799,
        longitude=-3.703583,
        server_base_url='http://localhost:8090/',
    )
    debit_wallet = Wallet.objects.filter(type__id='debit').first()
    city.wallet = debit_wallet
    city.save()


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0023_city'),
    ]

    operations = [
        migrations.RunPython(create_initial_city),
    ]