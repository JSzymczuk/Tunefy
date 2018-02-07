import os
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from tunefy_cms.file_manager import remove_field_file, remove_file
from tunefy_cms.forms import CreateSongForm
from tunefy_cms.models import Song
from tunefy_cms.views.search import get_paginated_context


default_page_size = 10


@staff_member_required
def index(request, page_number=1, page_size=default_page_size):
    context = get_paginated_context(Song.objects.all(), page_number, page_size)
    return render(request, 'tunefy_cms/song/index.html', context)


@staff_member_required
def create(request):
    if request.method == 'POST':
        form = CreateSongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song.index')
    else:
        form = CreateSongForm()
    return render(request, 'tunefy_cms/song/create.html', {
        'form': form
    })


@staff_member_required
def edit(request, id):
    artist = Song.objects.get(pk = id)
    if request.method == 'POST':
        form = CreateSongForm(request.POST, request.FILES, instance = artist)
        if form.is_valid():
            form.save()
            if 'audio' in form.changed_data:
                audio = form.initial['audio'].name
                remove_file(os.path.join(settings.MEDIA_ROOT, audio))
            return redirect('song.index')
    else:
        form = CreateSongForm(instance = artist)
    return render(request, 'tunefy_cms/song/edit.html', {
        'form': form,
        'song_id': id
    })


@staff_member_required
def delete(request, id):
    song = Song.objects.filter(id = id)
    remove_field_file(song.first().audio)
    song.delete()
    return redirect('song.index')

