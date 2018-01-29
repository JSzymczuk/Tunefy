from django.http import Http404
from django.shortcuts import render
from .models import Test
from django_user_agents.utils import get_user_agent


def index(request):
    return render(request, 'test.html', {})


def test(request):
    db_connect()
    return render(request, 'test.html', {
        'browser': get_user_agent(request).browser[0],
        'data': Test.objects.all()
    })


def insert(request, number, name):
    db_connect()
    entity = Test(number=number, name=name)
    entity.save()
    return render(request, 'index.html', context)
        'browser': get_user_agent(request).browser[0],
        'data': Test.objects.all()
    })
