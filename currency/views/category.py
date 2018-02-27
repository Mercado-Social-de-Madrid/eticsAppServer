# coding=utf-8
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from currency.forms.EntityForm import EntityForm
from currency.forms.category import CategoryForm
from currency.models import Category
from helpers import superuser_required


@superuser_required
def category_list(request):

    categories = Category.objects.all()
    params = { 'categories': categories, }

    return render(request, 'category/list.html', params)


@superuser_required
def add_category(request):

    if request.method == "POST":
        form = EntityForm(request.POST, request.FILES)

        if form.is_valid():
            category = form.save()
            messages.add_message( request, messages.SUCCESS, 'Categoría %s añadida con éxito' % category.name )
            return redirect('category_list')
        else:
            print form.errors.as_data()
    else:
        form = EntityForm()

    return render(request, 'category/add.html', {
        'is_new': True,
        'form': form
    })


@superuser_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    can_edit = request.user.is_superuser

    if not can_edit:
        messages.add_message(request, messages.ERROR, 'No tienes permisos para editar la categoría')
        return redirect('category_list')

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=category)

        if form.is_valid():
            category = form.save()
            messages.add_message(request, messages.SUCCESS, 'Categoría "{}" actualizada con éxito'.format(category.name.encode('utf-8')))
            return redirect('category_list')
        else:
            print form.errors.as_data()

    else:
        form = CategoryForm(instance=category)

    return render(request, 'category/edit.html', {
        'form': form,
        'category': category,
    })
