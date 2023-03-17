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

@login_required
def member_card(request):
    user_type, member = request.user.get_related_entity()

    member_data = {
        "city": member.city.id,
        "member_id": member.member_id
    }

    return render(request, 'member/card.html', {
        'user_type': user_type,
        'member_id': member.member_id,
        'display_name': member.display_name,
        'member_qr': json.dumps(member_data),
    })
