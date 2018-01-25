from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('cms/', include('tunefy_cms.urls')),
    path('', include('tunefy_cms.urls')),
    path('admin/', admin.site.urls),
]
