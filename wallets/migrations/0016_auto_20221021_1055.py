# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2022-10-21 10:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallets', '0015_payment_concept'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='pin_code',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='C\xf3digo PIN (hasheado)'),
        ),
    ]
