import requests
from django.conf.urls import url
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned, PermissionDenied
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.http import HttpMultipleChoices, HttpGone, HttpCreated, HttpAccepted, HttpForbidden, HttpBadRequest, \
    HttpUnauthorized
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
        total_amount = bundle.data['total_amount']
        currency_amount = bundle.data['currency_amount']
        concept = None if not 'concept' in bundle.data else bundle.data['concept']
        pin_code = bundle.data['pin_code']

        bundle.obj = Payment.objects.new_payment(sender, receiver, total_amount, currency_amount, concept, pin_code)

        return bundle

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(receiver=bundle.request.user).select_related('sender')

    def dehydrate(self, bundle):
        # Include the payment sender name
        user_type, sender_instance = bundle.obj.sender.get_related_entity()
        if sender_instance:
            bundle.data['sender'] =  str(sender_instance)
            bundle.data['user_type'] = user_type
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


class SentPaymentsResource(ModelResource):

    class Meta:
        queryset = Payment.objects.pending()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'sent_payment'
        collection_name = 'payments'
        excludes = []
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()


    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(sender=bundle.request.user).select_related('receiver')

    def dehydrate(self, bundle):
        # Include the payment sender name
        if bundle.obj.receiver.first_name or bundle.obj.receiver.last_name:
            bundle.data['receiver'] = bundle.obj.receiver.first_name + ' ' + bundle.obj.receiver.last_name
        else:
            bundle.data['receiver'] = bundle.obj.receiver.username
        return bundle


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
        bundle.data['has_pincode'] = bundle.obj.pin_code is not None

        return bundle

    def obj_get(self, bundle, **kwargs):
        try:
            wallet = Wallet.objects.get(user=bundle.request.user)
        except Wallet.DoesNotExist:
            raise NotFound("User has no associated wallet")

        return wallet

        # Part related with the child /offers resource

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/purchase%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('wallet_purchase'), name="api_wallet_purchase"),

            url(r"^(?P<resource_name>%s)/reset_pincode%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('reset_pincode'), name="api_reset_pincode"),
        ]

    def wallet_purchase(self, request, **kwargs):

        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)
        self.throttle_check(request)

        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE', 'application/json'))
        bundle = self.build_bundle(data=data, request=request)
        amount = data.get('amount', None)

        if not amount:
            return HttpGone()

        type, account = request.user.get_related_entity()
        if not account:
            return HttpGone()

        account_pk = None
        if type == 'entity':
            account_pk = account.cif
        elif type == 'person':
            account_pk = account.nif

        base_url = account.city.server_base_url
        api_url = '{}api/v1/account/{}/purchase/'.format(base_url, account_pk)

        r = requests.post(api_url, json={'amount': amount})
        if r.ok:
            return self.create_response(request, r.json())
        else:
            response = self.create_response(request, r.json(), HttpBadRequest)
            response.status_code = r.status_code
            return response


    def reset_pincode(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        self.is_authenticated(request)

        if request.user:
            data = self.deserialize(request, request.body,
                                    format=request.META.get('CONTENT_TYPE', 'application/json'))
            pincode = data.get('pincode', '')
            password = data.get('password', '')

            user = authenticate(username=request.user.username, password=password)
            if user:
                if user.is_active:
                    Wallet.update_user_pin_code(user=user, pin_code=pincode)
                    return self.create_response(request, {'success': True})
                else:
                    return self.create_response(request, {
                        'success': False,
                        'reason': 'disabled',
                    }, HttpForbidden)
            else:
                return self.create_response(request, {
                    'success': False,
                    'reason': 'incorrect',
                }, HttpUnauthorized)
        else:
            return self.create_response(request, {'success': False}, HttpUnauthorized)