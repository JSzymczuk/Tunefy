from django.shortcuts import render, redirect
from tunefy_cms.forms import CreateAlbumForm
from tunefy_cms.models import Album


def index(request):
    return render(request, 'album/index.html', {
        'albums': Album.objects.all()
    })


def create(request):
    if request.method == 'POST':
        form = CreateAlbumForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('album.index')
    else:
        form = CreateAlbumForm()
    return render(request, 'album/create.html', {
        'form': form
    })