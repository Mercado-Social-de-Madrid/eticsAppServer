from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from currency.models import Category


class CategoriesResource(ModelResource):

    class Meta:
        queryset = Category.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'categories'
        collection_name = 'categories'
        excludes = []

        authentication = Authentication()
        authorization = Authorization()
