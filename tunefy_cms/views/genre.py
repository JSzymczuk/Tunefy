from django.shortcuts import render, redirect
from tunefy_cms.forms import GenreForm
from tunefy_cms.models import Genre


def index(request):
    return render(request, 'genre/index.html', {
        'genres': Genre.objects.all()
    })


def create(request):
    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('genre.index')
    else:
        form = GenreForm()
    return render(request, 'genre/create.html', {
        'form': form
    })


def edit(request, id):
    genre = Genre.objects.get(pk = id)
    if request.method == 'POST':
        form = GenreForm(request.POST, request.FILES, instance = genre)
        if form.is_valid():
            form.save()
            return redirect('genre.index')
    else:
        form = GenreForm(instance = genre)
    return render(request, 'genre/edit.html', {
        'form': form,
        'genre_id': id
    })


def delete(request, id):
    Genre.objects.filter(id = id).delete()
    return redirect('genre.index')
