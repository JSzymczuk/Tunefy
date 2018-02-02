import os
from django.conf import settings
from django.shortcuts import render, redirect
from tunefy_cms.file_manager import remove_field_file, remove_file
from tunefy_cms.forms import CreateArtistForm
from tunefy_cms.models import Artist


def index(request):
    return render(request, 'artist/index.html', {
        'artists': Artist.objects.all()
    })


def create(request):
    if request.method == 'POST':
        form = CreateArtistForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('artist.index')
    else:
        form = CreateArtistForm()
    return render(request, 'artist/create.html', {
        'form': form
    })


def edit(request, id):
    artist = Artist.objects.get(pk = id)
    if request.method == 'POST':
        form = CreateArtistForm(request.POST, request.FILES, instance = artist)
        if form.is_valid():
            if form.initial_thumb:
                initial_thumb = form.initial_thumb.name
                initial_image = form.initial['image'].name
            form.save()
            if 'image' in form.changed_data:
                 remove_file(os.path.join(settings.MEDIA_ROOT, initial_thumb))
                 remove_file(os.path.join(settings.MEDIA_ROOT, initial_image))
            return redirect('artist.index')
    else:
        form = CreateArtistForm(instance = artist)
    return render(request, 'artist/edit.html', {
        'form': form,
        'artist_id': id
    })


def delete(request, id):
    artist = Artist.objects.filter(id = id)
    remove_image(artist.first())
    artist.delete()
    return redirect('artist.index')


def remove_image(artist):
    remove_field_file(artist.image)
    remove_field_file(artist.thumb)
