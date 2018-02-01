from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from offers.models import Offer
from wallets.models import Wallet, Payment


def index(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):
    UserModel = get_user_model()
    type, entity = UserModel.get_related_entity(request.user)

    params = {}
    if type == 'entity':
        params['type'] = type
        params['entity'] = entity

        params['num_offers'] = Offer.objects.current(entity=entity).count()
        wallet = Wallet.objects.filter(user=request.user).first()
        params['balance'] = wallet.balance

        params['pending_payments'] = Payment.objects.pending(user=request.user)


    return render(request, 'profile/index.html', params)
