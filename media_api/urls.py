from django.urls import path
from .views import UploadMediaView, DeleteMediaView

urlpatterns = [
    path("upload/", UploadMediaView.as_view()),
    path("delete/", DeleteMediaView.as_view()),
]