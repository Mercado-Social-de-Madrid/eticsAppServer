# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse

import helpers
from currency.models import Entity
from offers.forms.offerform import OfferForm
from offers.models import Offer


@login_required
def user_offers(request):
    type, entity = get_user_model().get_related_entity(request.user)
    if type == 'entity':
        return redirect('entity_offers', entity_pk= entity.pk)
    elif type == 'person':
        messages.add_message(request, messages.ERROR, 'No tienes permisos para gestionar ofertas')
        return redirect('dashboard')
    else:
        return redirect('dashboard')

@login_required
def entity_offers(request, entity_pk):
    entity = get_object_or_404(Entity, pk=entity_pk)
    is_owner = request.user == entity.user

    if not is_owner and not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para ver las ofertas de esta entitdad')
        return redirect('entity_detail', pk=entity.pk)

    current_offers = Offer.objects.current(entity=entity)
    future_offers = Offer.objects.future(entity=entity)
    past_offers = Offer.objects.past(entity=entity)

    return render(request, 'offers/entity_list.html', {
        'entity': entity,
        'current_offers': current_offers,
        'future_offers':future_offers,
        'past_offers':past_offers,
        'is_offers_owner': is_owner
    })

@login_required
def add_offer(request, entity_pk):
    entity = get_object_or_404(Entity, pk=entity_pk)
    can_edit = request.user.is_superuser or request.user == entity.user

    if not can_edit:
        return redirect(reverse('entity_detail', kwargs={'entity_pk': entity.pk}) + '?permissions=false')

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.entity = entity
            offer.save()

            return redirect('entity_offers', entity_pk=entity.pk)

    else:
        form = OfferForm()

    return render(request, 'offers/edit.html', {
        'entity': entity,
        'form': form,
        'is_new': True
    })


@login_required
def offer_detail(request, entity_pk, offer_pk):
    entity = get_object_or_404(Entity, pk=entity_pk)
    offer = get_object_or_404(Offer, pk=offer_pk)

    can_edit = request.user.is_superuser or request.user == entity.user

    return render(request, 'offers/detail.html', {
        'entity': entity,
        'offer': offer,
        'can_edit':can_edit
    })

@login_required
def list_offers(request):

    offers = Offer.objects.all().order_by('-published_date').select_related('entity')
    page = request.GET.get('page')
    offers = helpers.paginate(offers, page, elems_perpage=6)

    params = {
        'ajax_url': reverse('list_offers'),
        'offers': offers,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'offers/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'offers/list.html', params)




@login_required
def offer_edit(request, entity_pk, offer_pk):
    entity = get_object_or_404(Entity, pk=entity_pk)
    offer = get_object_or_404(Offer, pk=offer_pk)
    can_edit = request.user.is_superuser or request.user == entity.user

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la oferta')
        return redirect('offer_detail', entity_pk=entity.pk, offer_pk=offer.pk )

    if request.method == "POST":
        form = OfferForm(request.POST, request.FILES, instance=offer)
        if form.is_valid():
            offer = form.save(commit=False)
            offer.entity = entity
            offer.save()

            return redirect('offer_detail', entity_pk=entity.pk, offer_pk=offer.pk)

    else:
        form = OfferForm(instance=offer)

    return render(request, 'offers/edit.html', {
        'offer': offer,
        'entity': entity,
        'form': form
    })