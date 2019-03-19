from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from api.cities import CitiesResource
from currency.models import Person


class PersonsResource(ModelResource):

    city = fields.ForeignKey(CitiesResource, 'city', full=False, null=True)

    class Meta:
        queryset = Person.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'persons'
        collection_name = 'persons'
        excludes = ['user']

        authentication = Authentication()
        authorization = Authorization()

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url
        return bundle

    def hydrate(self, bundle):
        if bundle.obj.profile_image:
            del bundle.obj.profile_image
