from django.conf.urls import url
from . import views

app_name = 'wallets'

urlpatterns = [

    url(r'^payments/$', views.pending_payments, name='pending_payments'),
    url(r'^payments/new/$', views.SelectPaymentReceiverView.as_view(), name='new_payment'),
    url(r'^payments/new/(?P<pk>[0-9a-f-]+)/$', views.new_payment, name='create_payment'),
    url(r'^payments/admin$', views.admin_payments, name='admin_payments'),
    url(r'^payments/(?P<pk>[0-9a-f-]+)/$', views.payment_detail, name='payment_detail'),

    url(r'^wallet/$', views.user_wallet, name='user_wallet'),
    url(r'^wallet/admin/$', views.WalletListView.as_view(), name='admin_wallet'),
    url(r'^wallet/(?P<pk>[0-9a-f-]+)/$', views.wallet_detail, name='wallet_detail'),
    url(r'^wallet/types/$', views.wallet_types_list, name='wallet_types_list'),
    url(r'^transactions/$', views.TransactionsListView.as_view(), name='transaction_list'),
    url(r'^transactions/bulk/$', views.BulkTransaction.as_view(), name='bulk_transaction'),
    url(r'^transactions/new/$', views.new_transaction, name='new_transaction'),

]