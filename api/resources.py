from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from currency.models import Entity, Offer


class EntitiesResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'entities'
        collection_name = 'entities'
        excludes = ['user']

        authentication = Authentication()
        authorization = Authorization()

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url
        return bundle


class OffersResource(ModelResource):

    entity = fields.ForeignKey(EntitiesResource, 'entity', full=False, null=True)

    class Meta:
        queryset = Offer.objects.current()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'offers'
        collection_name = 'offers'
        excludes = ['user']

        authentication = Authentication()
        authorization = Authorization()


    def dehydrate(self, bundle):
        # Add thumbnail field
        if bundle.obj.banner_thumbnail:
            bundle.data['banner_thumbnail'] = bundle.obj.banner_thumbnail.url

        # Remove the URI of the entity with just the id
        if bundle.obj.entity:
            bundle.data['entity'] = bundle.obj.entity.id
        return bundle