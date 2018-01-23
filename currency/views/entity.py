from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from currency.models import Entity, Gallery, GalleryPhoto


from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from currency.forms.EntityForm import EntityForm
from currency.forms.galleryform import PhotoGalleryForm
from currency.models import Entity, Gallery, GalleryPhoto


@login_required
def entity_detail(request, pk):

    entity = get_object_or_404(Entity, pk=pk)
    gallery = entity.gallery.photos.all()

    can_edit = False
    if request.user.is_authenticated and (request.user.is_superuser or request.user == entity.owner):
        can_edit = True

    return render(request, 'entity/detail.html', { 'entity': entity, 'gallery': gallery, 'can_edit': can_edit })


@login_required
def entity_edit(request, pk):

    entity = get_object_or_404(Entity, pk=pk)
    gallery = entity.gallery
    can_edit = False
    if request.user.is_superuser or request.user == entity.owner:
        can_edit = True

    if not can_edit:
        return redirect(reverse('entity_detail', kwargs={'pk':entity.pk} ) + '?permissions=false')

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

    return render(request, 'entity/edit.html', { 'form': form, 'gallery_formset':gallery_formset, 'entity': entity })
