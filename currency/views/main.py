from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    return render(request, 'index.html', {})


@login_required
def profile(request):

    params = {}

    return render(request, 'profile/index.html', params)
