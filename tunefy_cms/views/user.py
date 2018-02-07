from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from tunefy_cms.views.search import get_paginated_context


default_page_size = 10


@staff_member_required
def index(request, page_number=1, page_size=default_page_size):
    context = get_paginated_context(User.objects.all(), page_number, page_size)
    return render(request, 'tunefy_cms/user/index.html', context)


@staff_member_required
def edit(request, id):
    user = User.objects.filter(id=id).first()
    if request.user != user:
        user.is_staff = not user.is_staff
        user.save()
    return redirect('user.index')


@staff_member_required
def delete(request, id):
    user = User.objects.filter(id = id).first()
    if request.user != user and not user.is_staff:
        user.delete()
    return redirect('user.index')
