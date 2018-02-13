from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from tunefy_cms.file_manager import remove_field_file, edit_image_thumb
from tunefy_cms.forms import CreateArtistForm
from tunefy_cms.models import Artist
from tunefy_cms.views.search import get_paginated_context


default_page_size = 5


@staff_member_required
def index(request, page_number=1, page_size=default_page_size):
    context = get_paginated_context(Artist.objects.all(), page_number, page_size)
    return render(request, 'tunefy_cms/artist/index.html', context)


@staff_member_required
def create(request):
    if request.method == 'POST':
        form = CreateArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist.index')
    else:
        form = CreateArtistForm()
    return render(request, 'tunefy_cms/artist/create.html', {
        'form': form
    })


@staff_member_required
def edit(request, id):
    artist = Artist.objects.get(pk = id)
    if request.method == 'POST':
        form = CreateArtistForm(request.POST, request.FILES, instance=artist)
        if form.is_valid():
            edit_image_thumb(form)
            form.save()
            return redirect('artist.index')
    else:
        form = CreateArtistForm(instance=artist)
    return render(request, 'tunefy_cms/artist/edit.html', {
        'form': form,
        'artist_id': id
    })


@staff_member_required
def delete(request, id):
    artist = Artist.objects.filter(id=id)
    remove_image(artist.first())
    artist.delete()
    return redirect('artist.index')


def remove_image(artist):
    remove_field_file(artist.image)
    remove_field_file(artist.thumb)
