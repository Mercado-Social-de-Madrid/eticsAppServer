from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect

from currency.forms.PersonForm import PersonForm
from currency.models import Person

@login_required
def user_profile(request):
    person = get_object_or_404(Person, user=request.user)
    can_edit = request.user.is_superuser or request.user == person.user
    form = PersonForm(instance=person)
    return render(request, 'profile/detail.html', {
        'person': person,'form':form, 'can_edit':can_edit
    })


@login_required
def profile_detail(request, pk):
    person = get_object_or_404(Person, pk=pk)
    can_edit = request.user.is_superuser or request.user == person.user
    form = PersonForm(instance=person)
    return render(request, 'profile/detail.html', {
        'person': person, 'form':form, 'can_edit':can_edit
    })


@login_required
def profile_edit(request, pk):
    person = get_object_or_404(Person, pk=pk)
    can_edit = request.user.is_superuser or request.user == person.user

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar esta consumidora')
        return redirect('profile_detail', pk=person.pk )


    if request.method == "POST":
        form = PersonForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            person = form.save(commit=False)
            person.save()
            form.save_m2m()

            return redirect('profile_detail', pk=person.pk)
        else:
            print form.errors.as_data()
    else:
        form = PersonForm(instance=person)

    return render(request, 'profile/edit.html', {
        'form': form,
        'person': person,
        'can_edit':can_edit
    })