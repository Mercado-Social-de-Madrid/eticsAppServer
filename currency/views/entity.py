from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from currency.forms.EntityForm import EntityForm
from currency.models import Entity


@login_required
def entity_edit(request, pk):
    entity = get_object_or_404(Entity, pk=pk)

    can_edit = False
    if request.user.is_superuser or request.user == entity.owner:
        can_edit = True

    if not can_edit:
        return redirect(reverse('entity_detail', kwargs={'pk':entity.pk} ) + '?permissions=false')

    if request.method == "POST":
        form = EntityForm(request.POST, request.FILES, instance=entity)
        if form.is_valid():
            entity = form.save()
            return redirect('entity_detail', pk=entity.pk)
        else:
            print form.errors.as_data()
    else:
        form = EntityForm(instance=entity)
    return render(request, 'entity/edit.html', { 'form': form, 'entity': entity })
