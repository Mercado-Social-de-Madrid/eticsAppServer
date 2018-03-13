# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from wallets.models import Wallet, Payment, Transaction, WalletType

admin.site.register(WalletType)
admin.site.register(Wallet)
admin.site.register(Transaction)

def accept(modeladmin, request, queryset):
    for payment in queryset:
        payment.accept_payment()
accept.short_description = "Aceptar pago"

def cancel(modeladmin, request, queryset):
    for payment in queryset:
        payment.cancel_payment()
cancel.short_description = "Cancelar pago"

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'total_amount', 'currency_amount', 'status']
    ordering = ['status']
    actions = [accept, cancel]

admin.site.register(Payment, PaymentAdmin)