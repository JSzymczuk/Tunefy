import os
from PIL import ImageOps, Image
from io import BytesIO
from datetime import datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.core.files.uploadedfile import SimpleUploadedFile

from tunefy import settings

THUMBNAIL_SIZE = (160, 160)


def file_generate_name():
    return datetime.now().__format__("%Y%m%d_%H%M%S%f")


def get_uploaded_file_path(folder):
    return folder + '/' +  file_generate_name()


def path_and_rename(path):
    def wrapper(obj, filename):
        ext = filename.split('.')[-1]
        filename = '{}.{}'.format(file_generate_name(), ext)
        return os.path.join(path, filename)
    return wrapper


def wrapper(obj, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(file_generate_name(), ext)
    return os.path.join('', filename)


def create_thumb(obj):
    if not obj.image:
        return

    # DJANGO_TYPE = obj.image.file.content_type
    #
    # if DJANGO_TYPE == 'image/jpeg':
    #     PIL_TYPE = 'jpeg'
    #     FILE_EXTENSION = 'jpg'
    # elif DJANGO_TYPE == 'image/png':
    #     PIL_TYPE = 'png'
    #     FILE_EXTENSION = 'png'

    if obj.image.name.lower().endswith(".jpg"):
        PIL_TYPE = 'jpeg'
        FILE_EXTENSION = 'jpg'
        DJANGO_TYPE = 'image/jpeg'
    elif obj.image.name.lower().endswith(".png"):
        PIL_TYPE = 'png'
        FILE_EXTENSION = 'png'
        DJANGO_TYPE = 'image/png'

    image = ImageOps.fit(Image.open(BytesIO(obj.image.read())), THUMBNAIL_SIZE, Image.ANTIALIAS)

    temp_handle = BytesIO()
    image.save(temp_handle, PIL_TYPE)
    temp_handle.seek(0)

    suf = SimpleUploadedFile(os.path.split(obj.image.name)[-1], temp_handle.read(), content_type=DJANGO_TYPE)
    obj.thumb.save(FILE_EXTENSION, suf, save=False)


def edit_image_thumb(form):
    if form.initial_thumb:
        initial_thumb = form.initial_thumb.name
        initial_image = form.initial['image'].name
    if 'image' in form.changed_data:
        remove_file(os.path.join(settings.MEDIA_ROOT, initial_thumb))
        remove_file(os.path.join(settings.MEDIA_ROOT, initial_image))


def file_save(file, path):
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def remove_field_file(field):
    if field:
        field.delete()


def remove_file(path):
    if os.path.isfile(path):
        os.remove(path)

