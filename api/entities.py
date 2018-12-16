from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Q
from tastypie import fields
from tastypie.authentication import Authentication, MultiAuthentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL
from tastypie.http import HttpGone, HttpMultipleChoices
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from api.categories import CategoriesResource
from api.cities import CitiesResource
from api.resources import OffersResource
from currency.models import Entity, Gallery, GalleryPhoto
from offers.models import Offer


class PhotoGalleryResource(ModelResource):

    class Meta:
        queryset = GalleryPhoto.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'photo'
        collection_name = 'photos'
        excludes = ['title', 'id', 'uploaded']

        authentication = Authentication()
        authorization = Authorization()


class GalleryResource(ModelResource):
    photos = fields.ToManyField(PhotoGalleryResource, 'photos', full=True)

    class Meta:
        queryset = Gallery.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'gallery'
        collection_name = 'galleries'
        excludes = ['title', 'id']


        authentication = Authentication()
        authorization = Authorization()

class EntitySimpleResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'simple_entity'
        collection_name = 'simple_entity'
        fields = ['id', 'name', 'address', 'logo']

        authentication = Authentication()
        authorization = Authorization()

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url


        return bundle


class EntitiesDetailResource(ModelResource):
    offers = fields.ToManyField(OffersResource,
                                attribute=lambda bundle: Offer.objects.current().filter(entity=bundle.obj),
                                full=True, null=True)

    categories = fields.ToManyField(CategoriesResource, 'categories', full=False, null=True)
    city = fields.ForeignKey(CitiesResource, 'city', full=False, null=True)
    gallery = fields.ToOneField(GalleryResource, 'gallery', full=True, null=True)

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'entities'
        collection_name = 'entities'
        excludes = ['user']

        filtering = {
            'categories': ALL,
            'city': ('exact', ),
        }

        authentication = MultiAuthentication(ApiKeyAuthentication(), Authentication(), )
        authorization = Authorization()

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url

        if bundle.obj.city:
            bundle.data['city'] = bundle.obj.city.id

        if bundle.data['categories']:
            for i, cat in enumerate(bundle.data['categories']):
                bundle.data['categories'][i] = cat.split('/')[-2:][0]

        return bundle


    def apply_filters(self, request, applicable_filters):

        print applicable_filters
        if not 'city__exact' in applicable_filters:

            if request.user and request.user.is_authenticated():
                # if no city filter was applied, we get the user city
                rel_type, related = request.user.get_related_entity()
                if related:
                    applicable_filters['city__exact'] = related.city.id
            else:
                # default to Madrid
                applicable_filters['city__exact'] = 'ara'

        base_object_list = super(EntitiesDetailResource, self).apply_filters(request, applicable_filters)
        query = request.GET.get('q', None)
        filters = {}
        if query:
            qset = (
                Q(name__icontains=query, **filters) |
                Q(short_description__icontains=query, **filters) |
                Q(description__icontains=query, **filters) |
                Q(address__icontains=query, **filters)
            )
            base_object_list = base_object_list.filter(qset).distinct()
        return base_object_list.filter(**filters).distinct()


    # Part related with the child /offers resource
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/offers%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_offers'), name="api_get_entity_offers"),
        ]

    def get_offers(self, request, **kwargs):

        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            obj = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        offers = OffersResource()
        return offers.get_list(request, entity=obj.pk)
