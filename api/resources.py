from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from currency.models import Offer


class OffersResource(ModelResource):

    entity = fields.ForeignKey('api.entities.EntitiesResource', 'entity', full=False, null=True)

    class Meta:
        queryset = Offer.objects.current()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'offers'
        collection_name = 'offers'
        excludes = ['user']
        filtering = {
            'entity': ('exact',),
        }

        authentication = Authentication()
        authorization = Authorization()


    def build_filters(self, filters=None, **kwargs):
        filters = {} if filters is None else filters
        orm_filters = super(OffersResource, self).build_filters(filters)

        if 'q' in filters:
            orm_filters['title__icontains'] = filters['q']
        return orm_filters

    def dehydrate(self, bundle):
        # Add thumbnail field
        if bundle.obj.banner_thumbnail:
            bundle.data['banner_thumbnail'] = bundle.obj.banner_thumbnail.url

        # Remove the URI of the entity with just the id
        if bundle.obj.entity:
            bundle.data['entity'] = bundle.obj.entity.id
        return bundle