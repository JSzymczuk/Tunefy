from math import floor
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import loader
from django.urls import reverse
from tunefy_app.forms import RegistrationForm, LoginForm
from tunefy_cms.models import Song, Track, Artist, Album, Playlist, PlaylistElement
from mutagen.mp3 import MP3


# def add_to_history(response, url):
#     history = response.COOKIES.get('history')
#     if history is not None:
#         response.COOKIES.set('history', history + ";" + url)
#     else:
#         response.COOKIES.set(history, url)
#     return response
#
#
# def previous(request):
#     history = request.COOKIES.get('history')
#     if history is not None:
#         history = history.split(';')
#         lth = len(history)
#         if lth > 0
#             url = history[lth - 1]
#             history = ';'.join(history)
#         else:
#             url = 'index.html'
#     else:
#         url =
#     return response


@login_required(redirect_field_name=None)
def index(request):
    l = loader.get_template('tunefy_app/index.html')
    response = HttpResponse(l.render({}, request))
    response.delete_cookie("current_playlist")
    response.delete_cookie("track")
    response.delete_cookie("album")
    response.delete_cookie("playlist")
    return response


@login_required(redirect_field_name=None)
def search(request):
    # if request.method == 'POST':
    #     phrase = request.POST.get('phrase', '').lower()
        phrase = request.GET.get('phrase', '').lower()
        tracks = [t for t in Track.objects.all() if phrase in t.song.title.lower()]
        albums = [a for a in Album.objects.all() if phrase in a.name.lower()]
        artists = [a for a in Artist.objects.all() if phrase in a.name.lower()]
        return render(request, 'tunefy_app/search.html', {
            'tracks': tracks,
            'albums': albums,
            'artists': artists
        })
    # else:
    #     return render(request, 'tunefy_app/search.html', {})


@login_required(redirect_field_name=None)
def artist(request, id):
    artist = Artist.objects.filter(id=id).first()
    return render(request, 'tunefy_app/artist.html', {
        'artist': artist,
        'albums': Album.objects.filter(artist=artist).order_by('-date_released'),
        'tracks': [t for t in Track.objects.order_by('popularity').all() if artist in t.song.artists.all()][0:10]
    })


@login_required(redirect_field_name=None)
def album(request, id):
    album = Album.objects.filter(id=id).first()
    return render(request, 'tunefy_app/album.html', {
        'album': album,
        'tracks': [t for t in Track.objects.all() if t.album == album]
    })


@login_required(redirect_field_name=None)
def create_playlist(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name and not name.isspace():
            Playlist(name=name, owner=request.user).save()
    return redirect('playlist.index')


@login_required(redirect_field_name=None)
def delete_playlist(request, id):
    current_playlist = Playlist.objects.filter(id=id).first()
    if current_playlist and current_playlist.owner == request.user:
        current_playlist.delete()
    response = HttpResponseRedirect(reverse('playlist.index'))
    if request.COOKIES.get('current_playlist') == id:
        response.delete_cookie("current_playlist")
    return response


@login_required(redirect_field_name=None)
def select_playlist(request, id):
    current_playlist = Playlist.objects.filter(id=id).first()
    response = HttpResponseRedirect(reverse('playlist.index'))
    if current_playlist and current_playlist.owner == request.user:
        response.set_cookie("current_playlist", id)
    return response


@login_required(redirect_field_name=None)
def get_playlists(request):
    current_playlist = request.COOKIES.get('current_playlist')
    return render(request, 'tunefy_app/playlists.html', {
        'playlists': Playlist.objects.filter(owner=request.user).order_by('name').all(),
        'current_playlist': int(current_playlist) if current_playlist else None
    })


@login_required(redirect_field_name=None)
def get_playlist(request, id):
    playlist = Playlist.objects.filter(id=id).first()
    return render(request, 'tunefy_app/playlist.html', {
        'playlist': playlist,
        'elements': PlaylistElement.objects.filter(playlist=playlist).order_by('order').all()
    })


@login_required(redirect_field_name=None)
def add_track(request, id):
    current_playlist_id = request.COOKIES.get('current_playlist')
    if current_playlist_id:
        track = Track.objects.filter(id=id).first()
        current_playlist = Playlist.objects.filter(id=current_playlist_id).first()
        if track and current_playlist and current_playlist.owner == request.user:
            PlaylistElement(playlist=current_playlist, track=track,
                order=PlaylistElement.objects.filter(playlist=current_playlist).count()).save()
        return HttpResponseRedirect(reverse('playlist.index', kwargs={
            'id': int(current_playlist_id) if current_playlist_id else None
        }))
    return redirect('index')


@login_required(redirect_field_name=None)
def remove_track(request, id):
    element = PlaylistElement.objects.filter(id=id).first()
    if element:
        playlist = element.playlist
        if playlist.owner == request.user:
            element_order = element.order
            for playlist_element in PlaylistElement.objects.filter(playlist=playlist).all():
                if playlist_element.order > element_order:
                    playlist_element.order -= 1
                    playlist_element.save()
            element.delete()
    return HttpResponseRedirect(reverse('playlist.index', kwargs={ 'id': playlist.id }))


@login_required(redirect_field_name=None)
def play_track(request, track_id):
    track = Track.objects.filter(id=track_id).first()
    if track is not None and track.song is not None and track.song.audio is not None:
        response = HttpResponseRedirect(reverse('track.play'))
        response.set_cookie("track", track_id)
        response.delete_cookie("album")
        response.delete_cookie("playlist")
        return response
    return render(request, 'tunefy_app/player.html', {
        'track': None
    })


@login_required(redirect_field_name=None)
def play_album(request, album_id, track_id=-1):
    album = Album.objects.filter(id=album_id).first()
    if album is not None:
        if int(track_id) < 0:
            track = Track.objects.filter(album_id=album).order_by('order').first()
        else:
            track = Track.objects.filter(id=track_id).first()
        if track is not None\
                and track.album_id is album.id\
                and track.song is not None\
                and track.song.audio is not None:
            response = HttpResponseRedirect(reverse('track.play'))
            response.set_cookie("track", track.id)
            response.set_cookie("album", album.id)
            response.delete_cookie("playlist")
            return response
    return render(request, 'tunefy_app/player.html', {
        'track': None
    })


@login_required(redirect_field_name=None)
def play_playlist(request, playlist_id, element_id=-1):
    playlist = Playlist.objects.filter(id=playlist_id).first()
    if playlist is not None:
        if int(element_id) < 0:
            element = PlaylistElement.objects.filter(playlist=playlist).order_by('order').first()
        else:
            element = PlaylistElement.objects.filter(id=element_id).first()
        if element is not None\
                and element.track is not None\
                and element.track.song is not None\
                and element.track.song.audio is not None:
            response = HttpResponseRedirect(reverse('track.play'))
            response.set_cookie("track", element.id)
            response.delete_cookie("album")
            response.set_cookie("playlist", playlist.id)
            return response
    return render(request, 'tunefy_app/player.html', {
        'track': None
    })


@login_required(redirect_field_name=None)
def get_track(request):
    if 'track' not in request.COOKIES:
        return render(request, 'tunefy_app/player.html', {
            'track': None
        })
    if 'playlist' in request.COOKIES:
        track = PlaylistElement.objects.filter(id=request.COOKIES.get('track')).first().track
    else:
        track = Track.objects.filter(id=request.COOKIES.get('track')).first()
    audio = MP3(track.song.audio)
    try:
        len = audio.info.length
        minutes = floor(len / 60)
        seconds = int(len) % 60
    except:
        minutes = 0
        seconds = 0
    return render(request, 'tunefy_app/player.html', {
        'track': track,
        'minutes': minutes,
        'seconds': str(seconds).zfill(2),
        'volume': request.COOKIES.get('volume', 1)
    })


@login_required(redirect_field_name=None)
def play_next(request):
    response = HttpResponseRedirect(reverse('track.play'))
    if 'track' in request.COOKIES:
        #if track is not None:
        try:
            if 'album' in request.COOKIES:
                album = Album.objects.filter(id=request.COOKIES.get('album')).first()
                track = Track.objects.filter(id=request.COOKIES.get('track')).first()
                next_track = Track.objects.filter(album=album, order__gt=track.order).order_by('order').first()
                response.set_cookie("track", next_track.id)
            elif 'playlist' in request.COOKIES:
                #playlist = Playlist.objects.filter(id=request.COOKIES.get('playlist')).first()
                element = PlaylistElement.objects.filter(id=request.COOKIES.get('track')).first()
                #element = PlaylistElement.objects.filter(playlist=playlist, track=track).order_by('order').first()
                next_element = PlaylistElement.objects.filter(playlist=element.playlist, order__gt=element.order)\
                    .order_by('order').first()
                response.set_cookie("track", next_element.id)
            else:
                response.delete_cookie("track")
        except:
            response.delete_cookie("track")
        return response
    response.delete_cookie("track")
    return response


@login_required(redirect_field_name=None)
def play_prev(request):
    response = HttpResponseRedirect(reverse('track.play'))
    if 'track' in request.COOKIES:
        #if track is not None:
        try:
            if 'album' in request.COOKIES:
                album = Album.objects.filter(id=request.COOKIES.get('album')).first()
                track = Track.objects.filter(id=request.COOKIES.get('track')).first()
                next_track = Track.objects.filter(album=album, order__lt=track.order).order_by('-order').first()
                response.set_cookie("track", next_track.id)
            elif 'playlist' in request.COOKIES:
                element = PlaylistElement.objects.filter(id=request.COOKIES.get('track')).first()
                prev_element = PlaylistElement.objects.filter(playlist=element.playlist, order__lt=element.order)\
                    .order_by('-order').first()
                response.set_cookie("track", prev_element.id)
            else:
                response.delete_cookie("track")
        except:
            response.delete_cookie("track")
        return response
    response.delete_cookie("track")
    return response


@login_required(redirect_field_name=None)
def set_volume(request, volume):
    volume = min(1, max(0, float(volume)))
    response = HttpResponse('Volume changed to 0.')
    response.set_cookie('volume', volume)
    return response


def sign_in(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {
        'form': form
    })


@login_required(redirect_field_name=None)
def sign_out(request):
    logout(request)
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            User.objects.create_user(username, password=password)
            new_user = authenticate(username=username, password=password)
            login(request, new_user)
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {
        'form': form
    })
