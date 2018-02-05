from django.shortcuts import render
from tunefy_cms.models import Song, Track, Artist, Album


def index(request):
    return render(request, 'tunefy_app/index.html', {})


def search(request):
    if request.method == 'POST':
        phrase = request.POST.get('phrase', '').lower()
        tracks = [t for t in Track.objects.all() if phrase in t.song.title.lower()]
        return render(request, 'tunefy_app/search.html', {
            'tracks': tracks
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