

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
from currency.models import Entity
from currency.models.extend_user import get_user_by_related
from wallets.models import Payment


class PaymentsResource(ModelResource):

    class Meta:
        queryset = Payment.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'payment'
        collection_name = 'payments'
        excludes = []
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        print bundle
        print bundle.data

        sender = bundle.request.user
        receiver = bundle.data['receiver']
        total_amount =bundle.data['total_amount']
        currency_amount = bundle.data['currency_amount']

        bundle.obj = Payment.objects.new_payment(sender, receiver, total_amount, currency_amount)

        return bundle