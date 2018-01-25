from django.http import Http404
from django.shortcuts import render
from .models import Genre


def index(request):
    return render(request, 'index.html', { 'genres': Genre.objects.all() })
