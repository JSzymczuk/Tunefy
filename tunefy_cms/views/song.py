import os
from django.conf import settings
from django.shortcuts import render, redirect
from tunefy_cms.file_manager import remove_field_file, remove_file
from tunefy_cms.forms import CreateSongForm
from tunefy_cms.models import Song


def index(request):
    return render(request, 'song/index.html', {
        'songs': Song.objects.all()
    })


def create(request):
    if request.method == 'POST':
        form = CreateSongForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('song.index')
    else:
        form = CreateSongForm()
    return render(request, 'song/create.html', {
        'form': form
    })


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
    return render(request, 'song/edit.html', {
        'form': form,
        'song_id': id
    })


def delete(request, id):
    song = Song.objects.filter(id = id)
    remove_field_file(song.first().audio)
    song.delete()
    return redirect('song.index')

