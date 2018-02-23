# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from news.models import News


class NewsAdmin(admin.ModelAdmin):

    def pub_date(self, obj):
        return obj.published_date.strftime("%d/%M/%Y")


    list_display = ('pub_date', 'title')
    ordering = '-published_date',
    pub_date.short_description = 'Publicada'


admin.site.register(News, NewsAdmin)
