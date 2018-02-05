from django.shortcuts import render


def index(request):
    return render(request, 'tunefy_cms/home/index.html', {})