from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('', include('shop.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += (
        [path("admin/", admin.site.urls)]
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
