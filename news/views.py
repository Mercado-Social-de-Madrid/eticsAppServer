# coding=utf-8
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage, InvalidPage
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from helpers import superuser_required
import helpers
from currency.models import Entity, Gallery, Category
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


@superuser_required
def news_list(request):

    news = News.objects.all()

    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = helpers.get_query(query_string, ['name', 'description', 'short_description'])
        if entry_query:
            news = news.filter(entry_query)

    page = request.GET.get('page')
    news = helpers.paginate(news, page, elems_perpage=10)

    params = {
        'ajax_url': reverse('news_list'),
        'query_string': query_string,
        'news': news,
        'page': page
    }

    if request.is_ajax():
        response = render(request, 'news/search_results.html', params)
        response['Cache-Control'] = 'no-cache'
        response['Vary'] = 'Accept'
        return response
    else:
        return render(request, 'news/list.html', params)


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


