# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

# Create your views here.
from currency.models import Entity
from offers.models import Offer


@login_required
def entity_offers(request, pk):
    entity = get_object_or_404(Entity, pk=pk)

    user_offers = Offer.objects.filter(entity=entity)
    return render(request, 'offers/entity_list.html', {
        'entity': entity,
        'offers': user_offers
    })