from django.contrib.auth.models import User
from tastypie import fields
from tastypie.resources import ModelResource

from currency.models import Entity




class EntityResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'entities'
        collection_name = 'entities'
        excludes = ['description', 'user']

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url
        return bundle


class UserResource(ModelResource):
    entity = fields.ToOneField(EntityResource, 'entity', null=True)

    class Meta:
        queryset = User.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'users'
        collection_name = 'users'
        excludes = ['password', 'is_staff', ]