from django.contrib import admin
from django.urls import path, include

from media_api.views import serve_media


urlpatterns = [

    path(
        "admin/",
        admin.site.urls
    ),

    path(
        "api/media/",
        include("media_api.urls")
    ),

    path(
        "media/<path:path>",
        serve_media,
        name="serve_media"
    ),
]