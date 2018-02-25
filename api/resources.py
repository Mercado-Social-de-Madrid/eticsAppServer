from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from news.models import News
from offers.models import Offer


class OffersResource(ModelResource):

    entity = fields.ForeignKey('api.entities.EntitySimpleResource', 'entity', full=True, null=True)

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


        return bundle


class NewsResource(ModelResource):


    class Meta:
        queryset = News.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'news'
        collection_name = 'news'
        excludes = ['published_by']
        authentication = Authentication()
        authorization = Authorization()


    def dehydrate(self, bundle):
        # Add thumbnail field
        if bundle.obj.banner_thumbnail:
            bundle.data['banner_thumbnail'] = bundle.obj.banner_thumbnail.url

        return bundle