from django.core.management.base import BaseCommand

from wallets.models import Wallet, WalletType


class Command(BaseCommand):
    help = 'Move all consumers balances to admin account'

    def handle(self, *args, **options):

        consumer_wallet_type = WalletType.objects.get(id='default')
        consumer_wallets = Wallet.objects.filter(type=consumer_wallet_type)

        admin_madrid_wallet = Wallet.objects.get(id='632ffba0-7b8f-42f7-a1c9-d4f43a677237')

        concept = 'Movimiento de saldo de consumidora a cuenta del MES'

        positive_balance_wallets_count = 0
        sum = 0

        for wallet in consumer_wallets:
            amount = wallet.balance
            if amount > 0:
                try:
                    wallet.new_transaction(amount, admin_madrid_wallet, concept, made_byadmin=True,)
                    print(f'Transaction done: {wallet.user} - {amount}')
                    sum += amount
                    positive_balance_wallets_count += 1
                except Exception as e:
                    print(f'Error in transaction: {wallet.user} \n {e}')


        print(f'positive_balance_wallets_count: {positive_balance_wallets_count}\nSum: {sum}')