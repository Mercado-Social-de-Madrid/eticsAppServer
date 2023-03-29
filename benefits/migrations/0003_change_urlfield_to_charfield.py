# Generated by Django 3.2.18 on 2023-03-29 12:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('benefits', '0002_add_discount_links'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benefit',
            name='discount_link_entities',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link de descuento para entidades'),
        ),
        migrations.AlterField(
            model_name='benefit',
            name='discount_link_members',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Link de descuento para socias'),
        ),
    ]
