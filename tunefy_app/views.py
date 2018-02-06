from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from tunefy_cms.models import Song, Track, Artist, Album, Playlist, PlaylistElement


def index(request):
    return render(request, 'tunefy_app/index.html', {})


def search(request):
    if request.method == 'POST':
        phrase = request.POST.get('phrase', '').lower()
        tracks = [t for t in Track.objects.all() if phrase in t.song.title.lower()]
        albums = [a for a in Album.objects.all() if phrase in a.name.lower()]
        artists = [a for a in Artist.objects.all() if phrase in a.name.lower()]
        return render(request, 'tunefy_app/search.html', {
            'tracks': tracks,
            'albums': albums,
            'artists': artists
        })
    else:
        return render(request, 'tunefy_app/search.html', {})


def artist(request, id):
    artist = Artist.objects.filter(id=id).first()
    return render(request, 'tunefy_app/artist.html', {
        'artist': artist,
        'albums': Album.objects.filter(artist=artist).order_by('-date_released'),
        'tracks': [t for t in Track.objects.order_by('popularity').all() if artist in t.song.artists.all()][0:10]
    })


def album(request, id):
    album = Album.objects.filter(id=id).first()
    return render(request, 'tunefy_app/album.html', {
        'album': album,
        'tracks': [t for t in Track.objects.all() if t.album == album]
    })


def create_playlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name and not name.isspace():
            # ustalić użytkownika
            Playlist(name=name).save()
    return redirect('playlist.index')


def delete_playlist(request, id):
    current_playlist = Playlist.objects.filter(id=id).first()
    # sprawdzić czy należy do obecnego użytkownika
    if current_playlist:
        current_playlist.delete()
    response = HttpResponseRedirect(reverse('playlist.index'))
    if request.COOKIES.get('current_playlist') == id:
        response.delete_cookie("current_playlist")
    return response


def select_playlist(request, id):
    current_playlist = Playlist.objects.filter(id=id).first()
    # sprawdzić czy należy do obecnego użytkownika
    response = HttpResponseRedirect(reverse('playlist.index'))
    if current_playlist:
        response.set_cookie("current_playlist", id)
    return response


def get_playlists(request):
    current_playlist = request.COOKIES.get('current_playlist')
    return render(request, 'tunefy_app/playlists.html', {
        'playlists': Playlist.objects.order_by('name').all(),
        'current_playlist': int(current_playlist) if current_playlist else None
    })


def get_playlist(request, id):
    playlist = Playlist.objects.filter(id=id).first()
    return render(request, 'tunefy_app/playlist.html', {
        'playlist': playlist,
        'elements': PlaylistElement.objects.filter(playlist=playlist).order_by('order').all()
    })


def add_track(request, id):
    current_playlist_id = request.COOKIES.get('current_playlist')
    if current_playlist_id:
        track = Track.objects.filter(id=id).first()
        current_playlist = Playlist.objects.filter(id=current_playlist_id).first()
        if track and current_playlist:
            # znowu sprawdzić właściciela
            PlaylistElement(playlist=current_playlist, track=track,
                order=PlaylistElement.objects.filter(playlist=current_playlist).count()).save()
    return HttpResponseRedirect(reverse('playlist.index', kwargs={
        'id': int(current_playlist_id) if current_playlist_id else None
    }))


def remove_track(request, id):
    element = PlaylistElement.objects.filter(id=id).first()
    if element:
        playlist = element.playlist
        element_order = element.order
        for playlist_element in PlaylistElement.objects.filter(playlist=playlist).all():
            if playlist_element.order > element_order:
                playlist_element.order -= 1
                playlist_element.save()
        element.delete()
    return HttpResponseRedirect(reverse('playlist.index', kwargs={ 'id': playlist.id }))



