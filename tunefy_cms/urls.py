from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tunefy_cms.views import artist, genre, home, song

urlpatterns = [
    # path('articles/2003/', views.special_case_2003),
    # path('articles/<int:year>/', views.year_archive),
    # path('articles/<int:year>/<int:month>/', views.month_archive),
    # path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),

    path('artist/',              artist.index,   name='artist.index'),
    path('artist/create/',       artist.create,  name='artist.create'),
    path('artist/edit/<id>/',    artist.edit,    name='artist.edit'),
    path('artist/delete/<id>/',  artist.delete,  name='artist.delete'),

    path('genre/',               genre.index,    name='genre.index'),
    path('genre/create/',        genre.create,   name='genre.create'),
    path('genre/edit/<id>/',     genre.edit,     name='genre.edit'),
    path('genre/delete/<id>/',   genre.delete,   name='genre.delete'),

    path('song/',                song.index,     name='song.index'),
    path('song/create/',         song.create,    name='song.create'),
    path('song/edit/<id>/',      song.edit,      name='song.edit'),
    path('song/delete/<id>/',    song.delete,    name='song.delete'),

    path('', home.index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)