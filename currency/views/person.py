from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from currency.models import Person

@login_required
def user_profile(request):
    person = get_object_or_404(Person, user=request.user)
    return render(request, 'profile/detail.html', {
        'person': person,
    })

@login_required
def profile_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    return render(request, 'profile/detail.html', {
        'person': person,
    })