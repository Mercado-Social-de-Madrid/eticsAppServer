from random import choice
from string import ascii_lowercase

import requests
from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import MultipleObjectsReturned
from django.forms import model_to_dict
from tastypie import fields
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpForbidden, HttpUnauthorized, HttpBadRequest, HttpNotFound
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from api.accounts import gen_userwallet_data
from currency.forms.user import UserForm
from currency.models import City, PreRegisteredUser, Entity, Person
from currency.models.extend_user import get_user_by_related
from wallets.models import Wallet



class FetchResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'fetch'
        list_allowed_methods = ['post']
        detail_allowed_methods = ['get']
        excludes = ['password', 'is_staff', 'is_superuser', 'id']

        authentication = ApiKeyAuthentication()  # Endpoint based on ApiKey auth
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^fetch/$", self.wrap_view('fetch_account'), name='api_fetch_account'),
        ]

    def fetch_account(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        if not request.user.is_superuser:
            return HttpUnauthorized()


        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))

        instance = None
        if 'uuid' in data:
            instance = get_user_by_related(data['uuid'])

        if instance is None and 'cif' in data and data['cif'] is not None:
            try:
                entity = Entity.objects.get(cif=data['cif'], inactive=False)
                instance = entity.user
            except Entity.DoesNotExist:
                try:
                    person = Person.objects.get(nif=data['cif'], inactive=False)
                    instance = person.user
                except Person.DoesNotExist:
                    instance = None
                except MultipleObjectsReturned:
                    raise Exception("Duplicated person. Nif: {}. Email: {}".format(data['cif'], data['email']))

            except MultipleObjectsReturned:
                raise Exception("Duplicated entity. Cif: {}. Email: {}".format(data['cif'], data['email']))

        if instance is None and 'email' in data:
            instance = User.objects.filter(email=data['email']).first()
            if instance is None:
                instance = Person.objects.filter(email=data['email']).first()

        if instance is None:
            return HttpNotFound()

        response = gen_userwallet_data(instance)
        response['user'] = model_to_dict(instance)
        response['user']['is_registered'] = instance.is_registered()
        return self.create_response(request, response)