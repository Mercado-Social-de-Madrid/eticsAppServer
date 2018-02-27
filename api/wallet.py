from tastypie import fields
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.exceptions import NotFound
from tastypie.resources import ModelResource

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

        bundle.obj = Payment.objects.new_payment(sender, receiver, total_amount, currency_amount)

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
