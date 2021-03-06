# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-02-28 14:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('currency', '0020_profile_address'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entity',
            old_name='bonification_percent',
            new_name='bonus_percent_general'
        ),
        migrations.AlterField(
            model_name='entity',
            name='bonus_percent_general',
            field=models.FloatField(default=0, verbose_name='Porcentaje de bonificaci\xf3n general'),
        ),
        migrations.AddField(
            model_name='entity',
            name='bonus_percent_entity',
            field=models.FloatField(default=0, verbose_name='Porcentaje de bonificaci\xf3n a entidades'),
        ),
    ]
