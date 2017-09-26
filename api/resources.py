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
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url
        return bundle