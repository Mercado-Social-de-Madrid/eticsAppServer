# coding=utf-8
from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import EmptyPage, Paginator, PageNotAnInteger, InvalidPage
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

import helpers
from currency.forms.password import PasswordForm
from currency.forms.password_reset import CustomPasswordResetForm
from currency.forms.preregister import UserForm
from currency.forms.profile import ProfileForm
from currency.models import PreRegisteredUser
from offers.models import Offer
from wallets.models import Wallet, Payment


def index(request):
    if request.user.is_authenticated:
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
            params['sent_pending'] = Payment.objects.sent_pending(user=request.user)
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


def preregister(request, pk):

    preuser = PreRegisteredUser.objects.filter(id=pk).first()
    if preuser is None:
        return render(request, 'registration/preregister.html', {
            'badtoken': True,
        })

    user = preuser.user
    kind, instance = user.get_related_entity()

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user.username = form.cleaned_data.get('username', '')
            user.set_password(form.cleaned_data.get('password', ''))
            user.save()

            pin_code = form.cleaned_data.get('pincode', '')
            Wallet.update_user_pin_code(user=user, pin_code=pin_code)

            preuser.delete()
            messages.add_message(request, messages.SUCCESS, 'Datos de acceso modificados satisfactoriamente')
            return redirect('preregister_success')
    else:
        form = UserForm()


    return render(request, 'registration/preregister.html', {
        'form': form,
        'token': preuser.id,

        'instance': instance,
    })


def preregister_success(request):
    return render(request, 'registration/success.html', {
})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()

    else:
        profile_form = ProfileForm(instance=request.user)
    password_form = PasswordForm(user=request.user)

    return render(request, 'registration/profile.html',
                  {'profile_form': profile_form,
                   'password_form':password_form,
                   'profile_tab': True
                   })

@login_required
def profile_password(request):
    if request.method == 'POST':
        password_form = PasswordForm(data=request.POST, user=request.user)

        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('edit_user_profile')

    else:
        password_form = PasswordForm(user=request.user)

    profile_form = ProfileForm(instance=request.user)
    return render(request, 'registration/profile.html', {
            'profile_form': profile_form,
            'password_form':password_form,
            'password_tab':True
            })


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/txt_password_reset_email.txt'
    html_email_template_name = 'registration/html_password_reset_email.html'
    form_class = CustomPasswordResetForm
    #from_email = None
