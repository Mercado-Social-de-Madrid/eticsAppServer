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
    type, instance = UserModel.get_related_entity(request.user)

    params = { 'type': type }
    wallet = Wallet.objects.filter(user=request.user).first()
    params['balance'] = wallet.balance

    if type == 'entity':
        params['entity'] = instance
        params['num_offers'] = Offer.objects.current(entity=instance).count()
        params['pending_payments'] = Payment.objects.pending(user=request.user)
    elif type == 'person':
        params['type'] = type
        params['person'] = instance

    return render(request, 'profile/index.html', params)
