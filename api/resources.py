from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from currency.models import Entity

from accounts import *

class EntityResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'entities'
        collection_name = 'entities'
        excludes = ['description', 'user']

        authentication = Authentication()
        authorization = Authorization()

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url
        return bundle

