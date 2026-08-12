import os
import uuid
import mimetypes

from django.conf import settings
from django.http import FileResponse, JsonResponse, Http404
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# =========================================================
# UPLOAD MEDIA
# =========================================================

@method_decorator(csrf_exempt, name="dispatch")
class UploadMediaView(View):

    def post(self, request):

        file = request.FILES.get("file")

        if not file:
            return JsonResponse(
                {
                    "success": False,
                    "error": "No file provided"
                },
                status=400
            )

        folder = request.POST.get(
            "folder",
            "uploads"
        )

        # Folder path
        folder_path = os.path.join(
            settings.MEDIA_ROOT,
            folder
        )

        # Folder create
        os.makedirs(
            folder_path,
            exist_ok=True
        )

        # Original filename
        original_name = os.path.basename(
            file.name
        )

        # Agar extension missing hai
        if "." not in original_name:
            original_name = f"{original_name}.jpg"

        # Unique filename
        filename = (
            f"{uuid.uuid4().hex}_"
            f"{original_name}"
        )

        # Complete file path
        file_path = os.path.join(
            folder_path,
            filename
        )

        # Save file
        with open(
            file_path,
            "wb+"
        ) as destination:

            for chunk in file.chunks():
                destination.write(chunk)

        # Database/storage mein ye path save hoga
        relative_path = (
            f"{folder}/{filename}"
        )

        # Public URL
        media_url = (
            f"{settings.MEDIA_BASE_URL}"
            f"/media/{relative_path}"
        )

        return JsonResponse(
            {
                "success": True,
                "path": relative_path,
                "url": media_url
            }
        )


# =========================================================
# DELETE MEDIA
# =========================================================

@method_decorator(csrf_exempt, name="dispatch")
class DeleteMediaView(View):

    def delete(self, request):

        path = request.GET.get("path")

        if not path:
            return JsonResponse(
                {
                    "success": False,
                    "error": "Path is required"
                },
                status=400
            )

        file_path = os.path.abspath(
            os.path.join(
                settings.MEDIA_ROOT,
                path
            )
        )

        media_root = os.path.abspath(
            settings.MEDIA_ROOT
        )

        # Security check
        if not file_path.startswith(
            media_root + os.sep
        ):
            return JsonResponse(
                {
                    "success": False,
                    "error": "Invalid file path"
                },
                status=400
            )

        if not os.path.exists(file_path):

            return JsonResponse(
                {
                    "success": False,
                    "error": "File not found"
                },
                status=404
            )

        os.remove(file_path)

        return JsonResponse(
            {
                "success": True,
                "message": "File deleted"
            }
        )


# =========================================================
# SERVE MEDIA
# =========================================================

def serve_media(request, path):

    file_path = os.path.abspath(
        os.path.join(
            settings.MEDIA_ROOT,
            path
        )
    )

    media_root = os.path.abspath(
        settings.MEDIA_ROOT
    )

    if not file_path.startswith(
        media_root + os.sep
    ):
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid file path"
            },
            status=400
        )

    if not os.path.isfile(file_path):
        raise Http404(
            "Media file not found"
        )

    content_type, _ = mimetypes.guess_type(
        file_path
    )

    if not content_type:
        content_type = "image/jpeg"

    response = FileResponse(
        open(
            file_path,
            "rb"
        ),
        content_type=content_type
    )

    response["Content-Disposition"] = "inline"

    return response