# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from offers.models import Offer


class OffersAdmin(admin.ModelAdmin):

    def pub_date(self, obj):
        return obj.published_date.strftime("%d/%M/%Y")

    def begin_date_format(self, obj):
        return obj.begin_date.strftime("%d/%M/%Y") if obj.begin_date else ''

    def end_date_format(self, obj):
        return obj.end_date.strftime("%d/%M/%Y") if obj.end_date else ''

    list_display = ('entity', 'title', 'active', 'pub_date', 'begin_date_format', 'end_date_format')
    ordering = '-published_date',
    pub_date.short_description = 'Publicado'
    begin_date_format.short_description = 'Fecha inicio'
    end_date_format.short_description = 'Fecha fin'

admin.site.register(Offer, OffersAdmin)
