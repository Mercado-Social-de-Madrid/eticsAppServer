import requests
from django.conf.urls import url
from fcm_django.models import FCMDevice
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource

from currency.models import Entity, Person
from wallets.models import Wallet


class EntityResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['get', 'put']
        resource_name = 'entity'
        excludes = ['user']

        authentication = ApiKeyAuthentication()  # Endpoint based on ApiKey auth
        authorization = Authorization()

    def dispatch_list(self, request, **kwargs):
        return self.dispatch_detail(request, **kwargs)

    def put_detail(self, request, **kwargs):
        return self.patch_detail(request, **kwargs)

    def obj_get(self, bundle, **kwargs):
        try:
            entity = Entity.objects.get(user=bundle.request.user)
        except Entity.DoesNotExist:
            raise NotFound("User has no associated entity")

        return entity

    def hydrate(self, bundle):
        if bundle.request.user:
            bundle.obj.user = bundle.request.user
        return bundle


class PersonResource(ModelResource):
    fav_entities = fields.ManyToManyField(EntityResource, 'fav_entities', full=False)

    class Meta:
        queryset = Person.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['get', 'put']
        resource_name = 'profile'
        excludes = ['id']

        authentication = ApiKeyAuthentication()  # Endpoint based on ApiKey auth
        authorization = Authorization()

    def dispatch_list(self, request, **kwargs):
        return self.dispatch_detail(request, **kwargs)

    def put_detail(self, request, **kwargs):
        return self.patch_detail(request, **kwargs)

    def obj_get(self, bundle, **kwargs):
        try:
            person = Person.objects.get(user=bundle.request.user)
        except Person.DoesNotExist:
            raise NotFound("User has no associated person")

        return person


    def prepend_urls(self):
        return [
            url(r"^invite/$", self.wrap_view('invite'), name='api_invite'),
        ]

    def invite(self,  request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        print request.user

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        bundle = self.build_bundle(data=data, request=request)
        print bundle.request.user

        if request.user and request.user.is_authenticated():
            data = self.deserialize(request, request.body,
                                    format=request.META.get('CONTENT_TYPE', 'application/json'))
            email = data.get('email', '')
            account_pk = None
            type, account = request.user.get_related_entity()
            if type == 'entity':
                account_pk = account.cif
            elif type == 'person':
                account_pk = account.nif

            base_url = account.city.server_base_url
            api_url = '{}api/v1/account/{}/invite/'.format(base_url, account_pk)

            r = requests.post(api_url, json={'email': email})
            if r.ok:
                return self.create_response(request, r.json())
            else:
                response = self.create_response(request, r.json(), HttpBadRequest)
                response.status_code = r.status_code
                return response
        else:
            return self.create_response(request, {'success': False}, HttpBadRequest)


    def dehydrate(self, bundle):
        # Add thumbnail field
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url

        if bundle.data['fav_entities']:
            for i, fav in enumerate(bundle.data['fav_entities']):
                bundle.data['fav_entities'][i] = fav.split('/')[-2:][0]

        return bundle

    def hydrate(self, bundle):
        if bundle.request.user:
            bundle.obj.user = bundle.request.user

        if bundle.data['fav_entities']:
            for i, fav in enumerate(bundle.data['fav_entities']):
                bundle.data['fav_entities'][i] = Entity.objects.get(pk=bundle.data['fav_entities'][i])

        return bundle


class DeviceResource(ModelResource):

    class Meta:
        queryset = FCMDevice.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['get', 'put']
        resource_name = 'device'
        excludes = []

        authentication = ApiKeyAuthentication()  # Endpoint based on ApiKey auth
        authorization = Authorization()

    def dispatch_list(self, request, **kwargs):
        return self.dispatch_detail(request, **kwargs)

    def put_detail(self, request, **kwargs):
        return self.patch_detail(request, **kwargs)

    def obj_get(self, bundle, **kwargs):
        try:
            device = FCMDevice.objects.get(user=bundle.request.user)
        except FCMDevice.DoesNotExist:
            device = FCMDevice.objects.create(user=bundle.request.user)

        return device


    def hydrate(self, bundle):
        if bundle.request.user:
            bundle.obj.user = bundle.request.user
        return bundle