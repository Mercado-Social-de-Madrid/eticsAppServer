# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from wallets.models import Wallet, Payment, Transaction

admin.site.register(Wallet)
admin.site.register(Transaction)

def accept(modeladmin, request, queryset):
    for payment in queryset:
        payment.accept_payment()

accept.short_description = "Aceptar pago"

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'total_amount', 'status']
    ordering = ['status']
    actions = [accept]

admin.site.register(Payment, PaymentAdmin)