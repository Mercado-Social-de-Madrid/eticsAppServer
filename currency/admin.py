from django.contrib import admin

# Register your models here.
from currency.models import Entity, Category, Wallet, Offer

admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Wallet)

class OffersAdmin(admin.ModelAdmin):
    list_display = ('entity', 'title', 'active', 'published_date', 'begin_date', 'end_date')
    ordering = '-published_date',
   
admin.site.register(Offer, OffersAdmin)
