# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from wallets.models import Wallet

admin.site.register(Wallet)
