from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(value, key):
    return value.get(key)
