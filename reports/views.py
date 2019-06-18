# coding=utf-8
import datetime
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.db.models import Count
from django.db.models.functions import TruncDay
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic.list import MultipleObjectMixin, BaseListView

from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from helpers import superuser_required
import helpers
from currency.models import Entity, Gallery, Category, Person
from news.forms.NewsForm import NewsForm
from news.models import News
from offers.models import Offer


@login_required
def user_entity(request):
    type, entity = get_user_model().get_related_entity(request.user)
    if type == 'entity':
        return redirect('entity_detail', pk= entity.pk)
    else:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para gestionar una entidad')
        return redirect('dashboard')


def index(request):
    last = request.GET.get('last', 'month')
    query = days_query[last]
    today = datetime.date.today()
    since = today - datetime.timedelta(days=query)

    total_entities = Entity.objects.count()
    new_entities = Entity.objects.filter(registered__gte=since).order_by('-registered')
    new_entities = helpers.paginate(new_entities, 0, elems_perpage=6)

    total_persons = Person.objects.count()
    new_persons = Person.objects.filter(registered__gte=since).order_by('-registered')
    new_persons = helpers.paginate(new_persons, 0, elems_perpage=6)

    return render(request, 'reports/index.html', { 'last': last, 'total_entities':total_entities, 'total_persons':total_persons, 'persons':new_persons, 'entities':new_entities })


def entity_detail(request, pk):
    entity = get_object_or_404(Entity, pk=pk)
    gallery = entity.gallery.photos.all()
    current_offers = Offer.objects.current(entity=entity)
    is_owner = request.user.is_authenticated and (request.user == entity.user)
    can_edit = is_owner or request.user.is_superuser

    return render(request, 'entity/detail.html', {
        'entity': entity,
        'gallery': gallery,
        'offers': current_offers,
        'can_edit_entity': can_edit,
        'is_entity_owner':is_owner
    })


days_query = {
    '3month':90,
    'month': 30,
    'week': 7,
}


@superuser_required
def offers(request):

    last = request.GET.get('last', 'month')
    query = days_query[last]

    today = datetime.date.today()
    since = today - datetime.timedelta(days=query)

    published = Offer.objects.published_last_days(query)
    active = Offer.objects.active_last_days(query)
    entities = Entity.objects.filter(pk__in=published.values_list('entity').distinct() )

    daily = active.annotate(day=TruncDay('published_date')).values('day').annotate(total=Count('id')).order_by('day')

    params = {
        'ajax_url': reverse('news_list'),
        'published': published,
        'active':active,
        'date_ranges':{
            'start':since,
            'end':today
        },
        'entities':entities,
        'daily': daily,
        'last': last
    }

    if request.is_ajax():
        response = render(request, 'reports/offers_card.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'reports/offers.html', params)


@login_required
def news_edit(request, pk):

    entry = get_object_or_404(News, pk=pk)
    can_edit = request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la noticia')
        return redirect('dashboard')

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=entry)

        if form.is_valid():

            entry = form.save()
            return redirect('news_list')
        else:
            print form.errors.as_data()
    else:
        form = NewsForm(instance=entry)

    return render(request, 'news/edit.html', {
        'form': form,
        'news': entry
    })



@superuser_required
def add_news(request):
    can_edit = request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar noticias')
        return redirect('dashboard')

    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)

        if form.is_valid():
            entry = form.save(commit=False)
            entry.published_by = request.user
            entry.save()
            messages.add_message(request, messages.SUCCESS, 'Noticia añadida con éxito')
            return redirect('news_list')
        else:
            print form.errors.as_data()
    else:
        form = NewsForm()

    return render(request, 'news/edit.html', {
        'form': form
    })


@superuser_required
def news_delete(request, pk):

    entry = get_object_or_404(News, pk=pk)
    can_edit = request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la noticia')
        return redirect('dashboard')

    if request.method == "POST":
        entry.delete()
        return redirect('news_list')
    else:
        return render(request, 'news/delete.html', {
            'news': entry
        })


