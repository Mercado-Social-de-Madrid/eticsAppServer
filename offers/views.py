# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from fcm_django.models import FCMDevice

from currency.models import Entity
from offers.forms.offerform import OfferForm
from offers.models import Offer


@login_required
def entity_offers(request, pk):
    entity = get_object_or_404(Entity, pk=pk)

    current_offers = Offer.objects.current().filter(entity=entity)
    print current_offers
    return render(request, 'offers/entity_list.html', {
        'entity': entity,
        'current_offers': current_offers
    })

@login_required
def add_offer(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    can_edit = request.user.is_superuser or request.user == entity.owner

    if not can_edit:
        return redirect(reverse('entity_detail', kwargs={'pk': entity.pk}) + '?permissions=false')

    '''device = FCMDevice.objects.all().first()
    result = device.send_message(data={"test": "test"})
    print result

    result = device.send_message(title="Titulo", body="Probando, probando...")
    print result
    '''

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.entity = entity
            offer.save()

            return redirect('entity_offers', pk=entity.pk)
        else:
            print form.errors.as_data()
    else:
        form = OfferForm()

    return render(request, 'offers/edit.html', {
        'entity': entity,
        'form': form,
        'is_new': True
    })