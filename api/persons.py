from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource

from currency.models import Person


class PersonsResource(ModelResource):

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

