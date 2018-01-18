from django.contrib import admin

# Register your models here.
from currency.models import Entity, Category, Person, Gallery, GalleryPhoto

admin.site.register(Entity)
admin.site.register(Category)
admin.site.register(Person)
admin.site.register(Gallery)
admin.site.register(GalleryPhoto)