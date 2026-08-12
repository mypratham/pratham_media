from django.urls import path

from .views import (
    UploadMediaView,
    DeleteMediaView,
    serve_media,
)


urlpatterns = [
    path(
        "upload/",
        UploadMediaView.as_view(),
        name="upload_media",
    ),

    path(
        "delete/",
        DeleteMediaView.as_view(),
        name="delete_media",
    ),

    path(
        "media/<path:path>",
        serve_media,
        name="serve_media",
    ),
]