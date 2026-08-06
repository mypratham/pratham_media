from django.urls import path
from .views import UploadMediaView, DeleteMediaView

app_name = "media_api"

urlpatterns = [
    path("upload/", UploadMediaView.as_view(), name="upload"),
    path("delete/", DeleteMediaView.as_view(), name="delete"),
]