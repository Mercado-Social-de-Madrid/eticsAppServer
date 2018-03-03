from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse

import helpers
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
def profile_list(request):
    persons = Person.objects.all()
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = helpers.get_query(query_string, ['name', 'surname', 'email'])
        if entry_query:
            persons = persons.filter(entry_query)

    page = request.GET.get('page')
    persons = helpers.paginate(persons, page, elems_perpage=10)

    params = {
        'ajax_url': reverse('profile_list'),
        'query_string': query_string,
        'profiles': persons,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'profile/profile_query.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'profile/list.html', params)


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