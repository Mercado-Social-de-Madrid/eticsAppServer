# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-28 10:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0019_auto_20180227_1921'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Direcci\xf3n'),
        ),
        migrations.AlterField(
            model_name='person',
            name='surname',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Apellidos'),
        ),
    ]
