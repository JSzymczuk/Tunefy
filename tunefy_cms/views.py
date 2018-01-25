from django.http import Http404
from django.shortcuts import render
from .models import Genre
from django_user_agents.utils import get_user_agent


def index(request):
    context = {
        'browser': get_user_agent(request).browser[0],
        'genres': Genre.objects.all()
    }
    return render(request, 'index.html', context)
