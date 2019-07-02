# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import operator

import django_filters
from django.db.models import Q


class PreregisterFilter(django_filters.BooleanFilter):

    def filter(self,qs,value):
        if value in (None, ''):
            return qs
        elif value:
            return qs.filter(user__preregister__isnull=False)
        else:
            return qs.filter(user__preregister__isnull=True)
