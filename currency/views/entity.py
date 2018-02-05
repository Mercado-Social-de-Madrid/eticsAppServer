from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from currency.models import Entity, Gallery
from offers.models import Offer


@login_required
def user_entity(request):
    type, entity = get_user_model().get_related_entity(request.user)
    if type == 'entity':
        return redirect('entity_detail', pk= entity.pk)


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

            PhotoGalleryForm.save_galleryphoto(entity.gallery, gallery_formset)

            return redirect('entity_detail', pk=entity.pk)
        else:
            print form.errors.as_data()
            print gallery_formset.errors
    else:
        form = EntityForm(instance=entity)
        gallery_formset = gallery_factory(initial=initial_photos)

    return render(request, 'entity/edit.html', {
        'form': form,
        'gallery_formset':gallery_formset,
        'entity': entity,
        'can_edit_entity':can_edit
    })
