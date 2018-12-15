from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from currency.models import Category, City


class CitiesResource(ModelResource):

    class Meta:
        queryset = City.objects.all()
        include_resource_uri = True
        list_allowed_methods = ['get']
        resource_name = 'cities'
        collection_name = 'cities'
        excludes = []

        authentication = Authentication()
        authorization = Authorization()
