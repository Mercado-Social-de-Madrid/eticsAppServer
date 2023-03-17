import json

import django_filters
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django_filters.views import FilterView

import helpers
from currency.forms.PersonForm import PersonForm
from currency.models import Person, PreRegisteredUser
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers.mixins.SuperUserCheck import SuperUserCheck
from helpers.pdf import render_pdf_response


def get_card_data(user_type, member):
    member_data = {
        "city": member.city.id,
        "member_id": member.member_id
    }
    card_data = {
        'user_type': user_type,
        'member_id': member.member_id,
        'display_name': member.display_name,
        'member_qr': json.dumps(member_data),
    }

    if user_type is 'person':
        card_data['is_intercoop'] = member.is_intercoop
        card_data['profile_image'] = member.profile_image
    else:
        card_data['profile_image'] = member.logo

    return card_data

@login_required
def member_card(request):
    user_type, member = request.user.get_related_entity()
    card_data = get_card_data(user_type, member)
    return render(request, 'member/card.html', card_data)

@login_required
def member_card_pdf(request):
    user_type, member = request.user.get_related_entity()
    card_data = get_card_data(user_type, member)

    filename = 'carnet_mesm'
    return render_pdf_response(request, 'member/card_pdf.html',
               card_data, filename=filename)