from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

from currency.models import Wallet, Entity, Person


class WalletResource(ModelResource):

    class Meta:
        queryset = Wallet.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['get']
        resource_name = 'wallet'
        fields = ['id', 'balance', 'last_transaction']

        authentication = ApiKeyAuthentication()  # Endpoint based on ApiKey auth
        authorization = Authorization()

    def dispatch_list(self, request, **kwargs):
        return self.dispatch_detail(request, **kwargs)

    def obj_get(self, bundle, **kwargs):
        try:
            wallet = Wallet.objects.get(user=bundle.request.user)
        except Wallet.DoesNotExist:
            raise NotFound("User has no associated entity")

        print wallet.pk
        return wallet


class EntityResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['get', 'put']
        resource_name = 'entity'
        excludes = ['id']

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

    def hydrate(self, bundle):
        if bundle.request.user:
            bundle.obj.user = bundle.request.user
        return bundle