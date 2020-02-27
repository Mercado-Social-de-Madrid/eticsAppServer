# -*- coding: utf-8 -*-

import django_filters
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from django_filters.views import FilterMixin, FilterView

import helpers
from currency.custom_filters import PreregisterFilter
from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from currency.models import Entity, Gallery, Category, PreRegisteredUser
from helpers import superuser_required
from helpers.filters.LabeledOrderingFilter import LabeledOrderingFilter
from helpers.filters.SearchFilter import SearchFilter
from helpers.forms.BootstrapForm import BootstrapForm
from helpers.mixins.AjaxTemplateResponseMixin import AjaxTemplateResponseMixin
from helpers.mixins.ExportAsCSVMixin import ExportAsCSVMixin
from helpers.mixins.ListItemUrlMixin import ListItemUrlMixin
from helpers.mixins.SuperUserCheck import SuperUserCheck
from offers.models import Offer

class UserFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status']


class UserFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'name', 'email'], lookup_expr='in', label='Buscar...')
    o = LabeledOrderingFilter(fields=['name',  'date_joined', 'last_login'], field_labels={'name':'Nombre', 'last_login':'Ultimo login','date_joined':'Fecha de registro'})

    class Meta:
        model = Entity
        form = UserFilterForm
        fields = [ ]

class UserListView(SuperUserCheck, ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = User
    queryset = User.objects.filter(preregister__isnull=True)
    objects_url_name = 'entity_detail'
    template_name = 'user/list.html'
    ajax_template_name = 'user/query.html'
    filterset_class = UserFilter
    paginate_by = 7

    csv_filename = 'usuarios'
    available_fields = ['username', 'email', 'date_joined', 'last_login']



