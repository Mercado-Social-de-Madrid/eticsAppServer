from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django.shortcuts import render, redirect
from django.urls import reverse

import helpers
from offers.models import Offer
from wallets.models import Wallet, Payment


def index(request):
    if request.user.is_authenticated():
        return redirect('dashboard')
    else:
        return redirect('login')

@login_required
def profile(request):

    if request.user.is_superuser:
        return render(request, 'profile/admin_index.html', {})
    else:
        UserModel = get_user_model()
        type, instance = UserModel.get_related_entity(request.user)

        params = { 'type': type, 'permission_error': request.GET.get('permission') }
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

@login_required
def search_users(request):
    users = User.objects.all()
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET.get('q')
        entry_query = helpers.get_query(query_string, ['username', 'first_name', 'last_name', 'email'])
        if entry_query:
            users = users.filter(entry_query)

    page = request.GET.get('page')
    users = helpers.paginate(users, page, 5)

    params = {
        'ajax_url': reverse('search_users'),
        'query_string': query_string,
        'users': users,
        'page': page
    }

    response = render(request, 'profile/search_results.html', params)
    response['Cache-Control'] = 'no-cache'
    response['Vary'] = 'Accept'
    return response
