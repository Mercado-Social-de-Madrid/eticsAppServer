from django.db.models import Q
from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

from wallets.models import Payment, Transaction, Wallet


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



class TransactionsResource(ModelResource):
    class Meta:
        queryset = Transaction.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'transaction'
        collection_name = 'transactions'
        excludes = []
        always_return_data = True

        authentication = ApiKeyAuthentication()
        authorization = Authorization()



class WalletResource(ModelResource):
    transactions = fields.ToManyField(TransactionsResource,
                                attribute=lambda bundle: Transaction.objects.filter(
                                    Q(wallet_to=bundle.obj) | Q(wallet_from=bundle.obj)),
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

        for t in bundle.data['transactions']:
            if t.obj.wallet_from == bundle.obj:
                t.data['amount'] = -t.data['amount']

        return bundle

    def obj_get(self, bundle, **kwargs):
        try:
            wallet = Wallet.objects.get(user=bundle.request.user)
        except Wallet.DoesNotExist:
            raise NotFound("User has no associated wallet")

        return wallet
