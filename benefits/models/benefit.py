import uuid

from django.db import models

from currency.models import Entity


class Benefit(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entity = models.OneToOneField(Entity, null=False, blank=False, related_name='benefit', on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    benefit_for_entities = models.TextField(null=True, blank=True, verbose_name='Ventajas para entidades')
    benefit_for_members = models.TextField(null=True, blank=True, verbose_name='Ventajas para socias')
    includes_intercoop_members = models.BooleanField(default=False, null=False, verbose_name='Incluye socias Intercoop')
    in_person = models.BooleanField(default=True, null=False, verbose_name='Solicitud física')
    online = models.BooleanField(default=True, null=False, verbose_name='Solicitud online')
    discount_code = models.CharField(max_length=20, null=True, blank=True, verbose_name='Código de descuento')
    discount_link = models.URLField(max_length=100, null=True, blank=True, verbose_name='Link de descuento')
    discount_link_text = models.CharField(max_length=50, null=True, blank=True, verbose_name='Texto del botón del link de descuento', default="Ir al descuento")
    active = models.BooleanField(default=True, null=False, verbose_name='Activa')

    class Meta:
        verbose_name = 'Ventaja'
        verbose_name_plural = 'Ventajas'
        ordering = ['-published_date']
