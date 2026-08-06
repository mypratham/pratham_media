import os
import uuid

from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UploadMediaView(APIView):

    authentication_classes = []
    permission_classes = []

    def post(self, request):

        file = request.FILES.get("file")

        folder = request.data.get("folder", "")

        if not file:

            return Response(
                {
                    "success": False,
                    "message": "No file uploaded"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        ext = os.path.splitext(file.name)[1]

        filename = f"{uuid.uuid4().hex}{ext}"

        save_dir = os.path.join(settings.MEDIA_ROOT, folder)

        os.makedirs(save_dir, exist_ok=True)

        filepath = os.path.join(save_dir, filename)

        with open(filepath, "wb+") as destination:

            for chunk in file.chunks():

                destination.write(chunk)

        relative_path = os.path.join(folder, filename).replace("\\", "/")

        return Response({

            "success": True,

            "path": relative_path,

            "url": request.build_absolute_uri(
                settings.MEDIA_URL + relative_path
            )

        })


class DeleteMediaView(APIView):

    authentication_classes = []
    permission_classes = []

    def delete(self, request):

        path = request.data.get("path")

        if not path:

            return Response(
                {
                    "success": False,
                    "message": "Path required"
                },
                status=400
            )

        file_path = os.path.join(settings.MEDIA_ROOT, path)

        if os.path.exists(file_path):

            os.remove(file_path)

            return Response({
                "success": True
            })

        return Response({
            "success": False,
            "message": "File not found"
        })