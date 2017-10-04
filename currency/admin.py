from django.contrib import admin

# Register your models here.
from currency.models import Entity, Category, Wallet, Offer

admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Wallet)

class OffersAdmin(admin.ModelAdmin):

    def pub_date(self, obj):
        return obj.published_date.strftime("%d/%M/%Y")

    def begin_date_format(self, obj):
        return obj.begin_date.strftime("%d/%M/%Y")

    def end_date_format(self, obj):
        return obj.end_date.strftime("%d/%M/%Y")

    list_display = ('entity', 'title', 'active', 'pub_date', 'begin_date_format', 'end_date_format')
    ordering = '-published_date',
    pub_date.short_description = 'Publicado'
    begin_date_format.short_description = 'Fecha inicio'
    end_date_format.short_description = 'Fecha fin'

admin.site.register(Offer, OffersAdmin)
