from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):
    UserModel = get_user_model()
    type, entity = UserModel.get_related_entity(request.user)

    params = {}
    if type != 'none':
        params['type'] = type
        params['entity'] = entity

    return render(request, 'profile/index.html', params)
