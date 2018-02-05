from django.shortcuts import render, redirect
from tunefy_cms.forms import GenreForm
from tunefy_cms.models import Genre
from tunefy_cms.views.search import get_paginated_context


default_page_size = 10


def index(request, page_number=1, page_size=default_page_size):
    context = get_paginated_context(Genre.objects.all(), page_number, page_size)
    return render(request, 'genre/index.html', context)


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
