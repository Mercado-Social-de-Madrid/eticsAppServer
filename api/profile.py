from django.urls import NoReverseMatch
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

from currency.models import Wallet, Entity


class WalletResource(ModelResource):

    class Meta:
        queryset = Wallet.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'wallet'
        fields = ['balance', 'last_transaction']
        excludes = ['id']

        authentication = ApiKeyAuthentication()  # Endpoint based on ApiKey auth
        authorization = Authorization()

    def dispatch(self, request_type, request, **kwargs):
        # Force this to be a single User object
        return super(WalletResource, self).dispatch('detail', request, **kwargs)

    def get_detail(self, request, **kwargs):
        # Place the authenticated user's id in the get detail request
        wallet = Wallet.objects.get(user=request.user)
        kwargs['id'] = wallet.pk

        return super(WalletResource, self).get_detail(request, **kwargs)


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

    def obj_get(self, bundle, **kwargs):
        try:
            entity = Entity.objects.get(user=bundle.request.user)
        except Entity.DoesNotExist:
            raise NotFound("User has no associated entity")

        return entity
