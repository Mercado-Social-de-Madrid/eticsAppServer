# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-30 13:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='active',
            field=models.BooleanField(default=True, verbose_name='Activa'),
        ),
    ]
