# coding=utf-8
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
from offers.models import Offer


@login_required
def user_entity(request):
    type, entity = get_user_model().get_related_entity(request.user)
    if type == 'entity':
        return redirect('entity_detail', pk= entity.pk)
    else:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para gestionar una entidad')
        return redirect('dashboard')


def entity_detail(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    if not entity.gallery:
        entity.gallery = Gallery.objects.create()
        entity.save()

    is_owner = request.user.is_authenticated and (request.user == entity.user)

    data = {
        'entity': entity,
        'gallery': entity.gallery.photos.all(),
        'offers': Offer.objects.current(entity=entity),
        'can_edit_entity': is_owner or request.user.is_superuser,
        'is_entity_owner': is_owner
    }

    if request.user.is_superuser:
        preuser = PreRegisteredUser.objects.filter(user=entity.user).first()
        if preuser:
            data['preregister_user'] = preuser


    return render(request, 'entity/detail.html', data)


@superuser_required
def entity_list(request):

    entities = Entity.objects.all()

    category_filter = request.GET.get('cat', None)
    if category_filter:
        entities = entities.filter(categories__pk=category_filter)

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = helpers.get_query(query_string, ['name', 'description', 'short_description'])
        if entry_query:
            entities = entities.filter(entry_query)

    page = request.GET.get('page')
    entities = helpers.paginate(entities, page, elems_perpage=6)

    params = {
        'ajax_url': reverse('entity_list'),
        'query_string': query_string,
        'entities': entities,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'entity/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        params['categories'] = Category.objects.all()
        return render(request, 'entity/list.html', params)


class EntityFilterForm(BootstrapForm):
    field_order = ['o', 'search', 'status', ]


class EntityFilter(django_filters.FilterSet):

    search = SearchFilter(names=['address', 'name', 'email'], lookup_expr='in', label='Buscar...')
    o = LabeledOrderingFilter(fields=['name', 'max_percent_payment', 'registered'], field_labels={'name':'Nombre', 'max_percent_payment':'Max. pago aceptado','registered':'Fecha de registro'})

    class Meta:
        model = Entity
        form = EntityFilterForm
        fields = {  }


class EntityListView(ExportAsCSVMixin, FilterView, ListItemUrlMixin, AjaxTemplateResponseMixin):

    model = Entity
    queryset = Entity.objects.all()
    objects_url_name = 'entity_detail'
    template_name = 'entity/list.html'
    ajax_template_name = 'entity/query.html'
    filterset_class = EntityFilter
    paginate_by = 7

    csv_filename = 'entidades'
    available_fields = ['cif', 'name', 'business_name', 'public_address', 'address',  'contact_email', 'contact_phone',
                        'postalcode', 'city', 'address', 'province', 'iban_code', 'registration_date', 'is_physical_store',
                        'bonus_percent_entity', 'bonus_percent_general', 'max_percent_payment', 'start_year']


@superuser_required
def add_entity(request):

    gallery_factory = PhotoGalleryForm.getGalleryFormset()
    initial_photos = PhotoGalleryForm.get_initial()

    if request.method == "POST":
        form = EntityForm(request.POST, request.FILES, initial={'is_new_entity':True})
        gallery_formset = gallery_factory(request.POST, request.FILES, initial=initial_photos)

        if form.is_valid() and gallery_formset.is_valid():
            entity = form.save(commit=False)

            owner_id = form.cleaned_data['owner_id']
            new_user_username = form.cleaned_data['new_user_username']
            new_user_password = form.cleaned_data['new_user_password']
            new_user_first_name = form.cleaned_data['new_user_first_name']
            new_user_last_name = form.cleaned_data['new_user_last_name']
            new_user_email = form.cleaned_data['new_user_email']

            if owner_id:
                user = User.objects.get(pk=owner_id)
                entity.user = user

            elif new_user_username and new_user_password:
                user_email = new_user_email if new_user_email else entity.email
                user, created = User.objects.get_or_create(username=new_user_username, email=user_email, password=new_user_password, first_name=new_user_first_name, last_name=new_user_last_name)
                entity.user = user
            else:
                entity.user = request.user

            gallery = Gallery.objects.create()
            entity.gallery = gallery
            entity.save()
            form.save_m2m()
            PhotoGalleryForm.save_galleryphoto(entity.gallery, gallery_formset)

            return redirect('entity_detail', pk=entity.pk)
        else:
            print form.errors.as_data()
            print gallery_formset.errors
    else:
        form = EntityForm(initial={'is_new_entity':True})
        gallery_formset = gallery_factory(initial=initial_photos)

    categories = Category.objects.all()

    return render(request, 'entity/add.html', {
        'is_new': True,
        'categories': categories,
        'form': form,
        'gallery_formset':gallery_formset
    })


@login_required
def entity_edit(request, pk):

    entity = get_object_or_404(Entity, pk=pk)
    gallery = entity.gallery
    can_edit = request.user.is_superuser or request.user == entity.user

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la entidad')
        return redirect('entity_detail', pk=entity.pk )

    gallery_factory = PhotoGalleryForm.getGalleryFormset(gallery)
    initial_photos = PhotoGalleryForm.get_initial(gallery)

    if request.method == "POST":
        form = EntityForm(request.POST, request.FILES, instance=entity)
        gallery_formset = gallery_factory(request.POST, request.FILES, initial=initial_photos)

        if form.is_valid() and gallery_formset.is_valid():

            entity = form.save(commit=False)
            if gallery is None:
                gallery = Gallery.objects.create()
            entity.gallery = gallery
            entity.save()
            form.save_m2m()

            PhotoGalleryForm.save_galleryphoto(entity.gallery, gallery_formset)

            return redirect('entity_detail', pk=entity.pk)
        else:
            print form.errors.as_data()
            print gallery_formset.errors
    else:
        form = EntityForm(instance=entity)
        gallery_formset = gallery_factory(initial=initial_photos)

    categories = Category.objects.all()

    return render(request, 'entity/edit.html', {
        'form': form,
        'gallery_formset':gallery_formset,
        'categories': categories,
        'entity': entity,
        'can_edit_entity':can_edit
    })


@xframe_options_exempt
def entity_map(request):

    entities = Entity.objects.all()
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = helpers.get_query(query_string, ['name', 'description', 'short_description'])
        if entry_query:
            entities = entities.filter(entry_query)

    city = request.GET.get('city', '')
    if city:
        entities = entities.filter(city=city)

    params = {
        'ajax_url': reverse('entity_list'),
        'query_string': query_string,
        'entities': entities,
    }



    return render(request, 'entity/map.html', params)