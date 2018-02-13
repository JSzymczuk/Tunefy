from itertools import zip_longest

import os

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from tunefy_cms.file_manager import remove_field_file, edit_image_thumb
from tunefy_cms.forms import CreateAlbumForm
from tunefy_cms.models import Album, Song, Track
from tunefy_cms.views.search import get_paginated_context


default_page_size = 5


@staff_member_required
def index(request, page_number=1, page_size=default_page_size):
    context = get_paginated_context(Album.objects.all(), page_number, page_size)
    context['tracks'] = Track.objects.all()
    return render(request, 'tunefy_cms/album/index.html', context)


@staff_member_required
def create(request):
    if request.method == 'POST':
        form = CreateAlbumForm([], request.POST, request.FILES)
        if form.is_valid():
            tracks = request.POST.getlist('tracks')
            all_songs = Song.objects.all()
            album = form.save()
            for counter, song_id in enumerate(tracks):
                Track.objects.create(order=counter + 1, album=album, song=all_songs.get(id=song_id)).save()
            return redirect('album.index')
    else:
        form = CreateAlbumForm([])
    return render(request, 'tunefy_cms/album/create.html', {
        'form': form,
        'songs': Song.objects.all()
    })


@staff_member_required
def delete(request, id):
    album = Album.objects.filter(id = id)
    remove_image(album.first())
    album.delete()
    return redirect('album.index')


@staff_member_required
def edit(request, id):
    album = Album.objects.get(pk = id)
    initial_tracks = Track.objects.filter(album = album).all()
    all_songs = Song.objects.all()
    if request.method == 'POST':
        form = CreateAlbumForm(initial_tracks, request.POST, request.FILES, instance = album)
        if form.is_valid():
            tracks = request.POST.getlist('tracks')
            for counter, (new_song_id, init_track) in enumerate(zip_longest(tracks, initial_tracks)):
                if init_track == None:
                    Track.objects.create(order = counter + 1, album = album, song = all_songs.get(id = new_song_id)).save()
                elif new_song_id == None:
                    init_track.delete()
                elif str(init_track.song_id) != new_song_id:
                    track = Track.objects.get(album=album, order=counter + 1)
                    track.song = all_songs.get(id = new_song_id)
                    track.save()
            edit_image_thumb(form)
            form.save()
            return redirect('album.index')
    else:
        form = CreateAlbumForm(initial_tracks, instance = album)
    return render(request, 'tunefy_cms/album/edit.html', {
        'album_id': id,
        'form': form,
        'songs': all_songs
    })


def remove_image(album):
    remove_field_file(album.image)
    remove_field_file(album.thumb)
