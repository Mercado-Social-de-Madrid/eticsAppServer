from django.conf.urls import url
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.forms import model_to_dict
from tastypie import fields
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpForbidden, HttpUnauthorized
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from currency.forms.user import UserForm
from currency.models import Wallet, Entity


class WalletResource(ModelResource):

    class Meta:
        queryset = Wallet.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'wallet'
        fields = ['balance', 'last_transaction']
        excludes = ['id']

        authentication = ApiKeyAuthentication()  # No need for auth, public resource
        authorization = Authorization()

    def dispatch(self, request_type, request, **kwargs):
        # Force this to be a single User object
        return super(WalletResource, self).dispatch('detail', request, **kwargs)

    def get_detail(self, request, **kwargs):
        # Place the authenticated user's id in the get detail request

        wallet = Wallet.objects.get(user=request.user)
        kwargs['id'] = wallet.pk


        return super(WalletResource, self).get_detail(request, **kwargs)


