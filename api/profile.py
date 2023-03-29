import base64

import requests
from django.conf import settings
from django.conf.urls import url
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from fcm_django.models import FCMDevice
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.http import HttpBadRequest
from tastypie.resources import ModelResource

from api.categories import CategoriesResource
from api.cities import CitiesResource
from currency.models import Entity, Person, City


class InviteResource(ModelResource):
    def prepend_urls(self):
        return [
            url(r"^invite/$", self.wrap_view('invite'), name='api_invite'),
        ]

    def invite(self,  request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        bundle = self.build_bundle(data=data, request=request)

        if request.user and request.user.is_authenticated:
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



class EntityResource(InviteResource):

    categories = fields.ToManyField(CategoriesResource, 'categories', full=False, null=True)
    city = fields.ForeignKey(CitiesResource, 'city', full=False, null=True)

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


    def dehydrate(self, bundle):
        # Add thumbnail field
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url

        bundle.data['qr_code'] = settings.BASESITE_URL + reverse('entity_qr_detail', args=(bundle.obj.pk,) )

        if bundle.obj.city:
            bundle.data['city'] = bundle.obj.city.id

        if bundle.data['categories']:
            for i, cat in enumerate(bundle.data['categories']):
                bundle.data['categories'][i] = cat.split('/')[-2:][0]

        return bundle


    def hydrate(self, bundle):
        if bundle.request.user:
            bundle.obj.user = bundle.request.user

        bundle.data['city'] = City.objects.get(pk=bundle.data['city'])

        if bundle.data['logo']:
            data_parts = bundle.data.get('logo', '').split(';')
            content_type = data_parts[0]
            if content_type in ['image/jpeg', 'image/png']:
                file_data = data_parts[1]
                image = SimpleUploadedFile('image.jpg', base64.b64decode(file_data), content_type=content_type)
                bundle.data['logo'] = image

        return bundle


class PersonResource(InviteResource):
    fav_entities = fields.ManyToManyField(EntityResource, 'fav_entities', full=False)
    city = fields.ForeignKey(CitiesResource, 'city', full=False, null=True)

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


    def dehydrate(self, bundle):
        # Add thumbnail field
        if bundle.obj.profile_thumbnail:
            bundle.data['profile_thumbnail'] = bundle.obj.profile_thumbnail.url

        if bundle.data['fav_entities']:
            for i, fav in enumerate(bundle.data['fav_entities']):
                bundle.data['fav_entities'][i] = fav.split('/')[-2:][0]

        if bundle.obj.city:
            bundle.data['city'] = bundle.obj.city.id

        return bundle

    def hydrate(self, bundle):
        if bundle.request.user:
            bundle.obj.user = bundle.request.user

        if bundle.data['fav_entities']:
            for i, fav in enumerate(bundle.data['fav_entities']):
                bundle.data['fav_entities'][i] = Entity.objects.get(pk=bundle.data['fav_entities'][i])

        if bundle.data['profile_image']:
            data_parts = bundle.data.get('profile_image', '').split(';')
            content_type = data_parts[0]
            if content_type in ['image/jpeg', 'image/png']:
                file_data = data_parts[1]
                image = SimpleUploadedFile('image.jpg', base64.b64decode(file_data), content_type=content_type)
                bundle.data['profile_image'] = image

        bundle.data['city'] = City.objects.get(pk=bundle.data['city'])

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