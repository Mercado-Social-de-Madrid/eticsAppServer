from django.contrib import admin

from benefits.models import Benefit


class BenefitsAdmin(admin.ModelAdmin):
    list_display = ('entity', 'benefit_for_entities', 'benefit_for_members', 'published_date', 'active')

admin.site.register(Benefit, BenefitsAdmin)
