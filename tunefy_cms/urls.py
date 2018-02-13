from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tunefy_cms.views import artist, genre, home, song, album, user

urlpatterns = [

    path('album/', album.index, name='album.index'),
    path('album/<int:page_number>/', album.index, name='album.index'),
    path('album/<int:page_size>/<int:page_number>/', album.index, name='album.index'),
    path('album/create/',        album.create,   name='album.create'),
    path('album/edit/<id>/',     album.edit,     name='album.edit'),
    path('album/delete/<id>/',   album.delete,   name='album.delete'),

    path('artist/', artist.index, name='artist.index'),
    path('artist/<int:page_number>/', artist.index, name='artist.index'),
    path('artist/<int:page_size>/<int:page_number>/', artist.index, name='artist.index'),
    path('artist/create/',       artist.create,  name='artist.create'),
    path('artist/edit/<id>/',    artist.edit,    name='artist.edit'),
    path('artist/delete/<id>/',  artist.delete,  name='artist.delete'),

    path('genre/',                   genre.index,    name='genre.index'),
    path('genre/<int:page_number>/', genre.index,    name='genre.index'),
    path('genre/<int:page_size>/<int:page_number>/', genre.index, name='genre.index'),
    path('genre/create/',        genre.create,   name='genre.create'),
    path('genre/edit/<id>/',     genre.edit,     name='genre.edit'),
    path('genre/delete/<id>/',   genre.delete,   name='genre.delete'),

    path('song/',                   song.index,    name='song.index'),
    path('song/<int:page_number>/', song.index,    name='song.index'),
    path('song/<int:page_size>/<int:page_number>/', song.index, name='song.index'),
    path('song/create/',         song.create,    name='song.create'),
    path('song/edit/<id>/',      song.edit,      name='song.edit'),
    path('song/delete/<id>/',    song.delete,    name='song.delete'),

    path('user/',                                   user.index,  name='user.index'  ),
    path('user/<int:page_number>/',                 user.index,  name='user.index'  ),
    path('user/<int:page_size>/<int:page_number>/', user.index,  name='user.index'  ),
    path('user/edit/<id>/',                         user.edit,   name='user.edit'   ),
    path('user/delete/<id>/',                       user.delete, name='user.delete' ),

    path('', home.index, name='cms')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
