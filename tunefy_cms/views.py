from django.http import Http404
from django.shortcuts import render
from .models import Test
from django_user_agents.utils import get_user_agent
from mongoengine import connect


def db_connect():
    connect(
        db='Tunefy',
        username='JSzymczuk',
        password='L@jkonik77',
        host='mongodb://JSzymczuk:L%40jkonik77@tunefy-shard-00-00-tf0rd.mongodb.net:27017,tunefy-shard-00-01-tf0rd.mongodb.net:27017,tunefy-shard-00-02-tf0rd.mongodb.net:27017/test?ssl=true&replicaSet=Tunefy-shard-0&authSource=admin'
    )


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
    return render(request, 'test.html', {
        'browser': get_user_agent(request).browser[0],
        'data': Test.objects.all()
    })
