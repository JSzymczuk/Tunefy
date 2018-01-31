from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from tunefy_cms.views import artist, home

urlpatterns = [
    # path('articles/2003/', views.special_case_2003),
    # path('articles/<int:year>/', views.year_archive),
    # path('articles/<int:year>/<int:month>/', views.month_archive),
    # path('articles/<int:year>/<int:month>/<slug:slug>/', views.article_detail),
    path('artists/', artist.index, name='artist.index'),
    path('artists/create/', artist.create, name='artist.create'),
    path('artists/edit/<id>/', artist.edit, name='artist.edit'),
    path('artists/delete/<id>/', artist.delete, name='artist.delete'),
    path('', home.index)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)