from django.urls import path
from django.conf.urls.static import static
from tunefy import settings
from tunefy_app import views

urlpatterns = [
    path('album/<id>/',   views.album,    name='album' ),
    path('artist/<id>/',  views.artist,   name='artist' ),
    path('search/',       views.search,   name='search' ),
    path('',              views.index,    name='index'  )

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)