from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, PermissionDenied
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.http import HttpMultipleChoices, HttpGone, HttpCreated, HttpAccepted, HttpForbidden
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash

from wallets.models import Payment, Wallet, TransactionLog


class PaymentsResource(ModelResource):

    class Meta:
        queryset = Payment.objects.pending()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'payment'
        collection_name = 'payments'
        excludes = []
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):

        sender = bundle.request.user
        receiver = bundle.data['receiver']
        total_amount =bundle.data['total_amount']
        currency_amount = bundle.data['currency_amount']
        pin_code = bundle.data['pin_code']

        bundle.obj = Payment.objects.new_payment(sender, receiver, total_amount, currency_amount, pin_code)

        return bundle

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(receiver=bundle.request.user).select_related('sender')

    def dehydrate(self, bundle):
        # Include the payment sender name
        if bundle.obj.sender.first_name or bundle.obj.sender.last_name:
            bundle.data['sender'] = bundle.obj.sender.first_name + ' ' + bundle.obj.sender.last_name
        else:
            bundle.data['sender'] = bundle.obj.sender.username
        return bundle

    # Part related with the child /offers resource
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/accept%s$" % (
            self._meta.resource_name, trailing_slash()),
                self.wrap_view('accept_payment'), name="api_accept_payment"),

            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/cancel%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('cancel_payment'), name="api_cancel_payment"),
        ]

    def accept_payment(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            payment = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")
        payment.accept_payment()
        return self.create_response(
                request, bundle,
                response_class = HttpCreated)

    def cancel_payment(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        try:
            bundle = self.build_bundle(data={'pk': kwargs['pk']}, request=request)
            payment = self.cached_obj_get(bundle=bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")
        payment.cancel_payment()
        return self.create_response(
                request, bundle,
                response_class = HttpCreated)


class TransactionLogResource(ModelResource):
    class Meta:
        queryset = TransactionLog.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'transaction'
        collection_name = 'transactions'
        excludes = ['id']
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(wallet__user=bundle.request.user)



class WalletResource(ModelResource):
    transaction_logs = fields.ToManyField(TransactionLogResource,
                                attribute=lambda bundle: TransactionLog.objects.filter(
                                   wallet=bundle.obj)[:10],
                                full=True, null=True)

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

    # Add logical amounts
    def dehydrate(self, bundle):
        print bundle.obj

        return bundle

    def obj_get(self, bundle, **kwargs):
        try:
            wallet = Wallet.objects.get(user=bundle.request.user)
        except Wallet.DoesNotExist:
            raise NotFound("User has no associated wallet")

        return wallet
