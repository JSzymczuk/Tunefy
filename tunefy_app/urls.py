from django.urls import path, include
from django.conf.urls.static import static
from tunefy import settings
from tunefy_app import views

urlpatterns = [

    path('playlist/create/',               views.create_playlist,  name='playlist.create'         ),
    path('playlist/delete/<id>/',          views.delete_playlist,  name='playlist.delete'         ),
    path('playlist/select/<id>/',          views.select_playlist,  name='playlist.select'         ),
    path('playlist/add_element/<id>/',     views.add_track,        name='playlist.add_element'    ),
    path('playlist/remove_element/<id>/',  views.remove_track,     name='playlist.remove_element' ),
    path('playlist/<id>/',                 views.get_playlist,     name='playlist.index'          ),
    path('playlist/',                      views.get_playlists,    name='playlist.index'          ),

    path('account/',          include('django.contrib.auth.urls')),
    path('account/register/', views.register, name='register'    ),

    path('play/<track_id>/<playlist_id>/<album_id>/', views.play_track, name='track.play'),
    path('play/<track_id>/<playlist_id>/',            views.play_track, name='track.play'),
    path('play/<track_id>/',                          views.play_track, name='track.play'),
    path('play/',                                     views.get_track,  name='track.play'),

    path('settings/volume/<volume>/', views.set_volume, name='volume.set'),

    path('album/<id>/',   views.album,    name='album'  ),
    path('artist/<id>/',  views.artist,   name='artist' ),
    path('search/',       views.search,   name='search' ),
    path('',              views.index,    name='index'  )

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)