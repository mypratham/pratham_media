import mimetypes
import os

from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html

from .models import MediaFile


@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):

    list_display = (
        "preview",
        "file_name",
        "file_path",
        "file_type",
        "file_size",
        "uploaded_at",
    )

    search_fields = ("file",)

    readonly_fields = (
        "preview",
        "file_path",
        "file_type",
        "file_size",
        "uploaded_at",
    )

    list_per_page = 50

    def get_queryset(self, request):
        """
        Admin open hote hi MEDIA_ROOT scan karke
        existing files ko database me add karega.
        """
        queryset = super().get_queryset(request)

        media_root = settings.MEDIA_ROOT

        if not media_root or not os.path.isdir(media_root):
            return queryset

        existing_files = set(
            queryset.values_list("file", flat=True)
        )

        new_files = []

        for root, dirs, files in os.walk(media_root):

            for filename in files:

                full_path = os.path.join(root, filename)

                relative_path = os.path.relpath(
                    full_path,
                    media_root
                ).replace(os.sep, "/")

                if relative_path not in existing_files:
                    new_files.append(
                        MediaFile(file=relative_path)
                    )

        if new_files:
            MediaFile.objects.bulk_create(
                new_files,
                ignore_conflicts=True
            )

        return super().get_queryset(request)

    def file_name(self, obj):
        return os.path.basename(obj.file.name)

    file_name.short_description = "Name"

    def file_path(self, obj):
        return obj.file.name

    file_path.short_description = "Path"

    def file_type(self, obj):
        mime_type, _ = mimetypes.guess_type(obj.file.name)
        return mime_type or "Unknown"

    file_type.short_description = "Type"

    def file_size(self, obj):
        try:
            size = obj.file.size
        except (FileNotFoundError, OSError):
            return "File missing"

        if size < 1024:
            return f"{size} B"

        if size < 1024 * 1024:
            return f"{size / 1024:.1f} KB"

        if size < 1024 * 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"

        return f"{size / (1024 * 1024 * 1024):.2f} GB"

    file_size.short_description = "Size"

    def preview(self, obj):
        if not obj.file:
            return "-"

        name = obj.file.name.lower()

        image_extensions = (
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
            ".svg",
        )

        media_base_url = settings.MEDIA_BASE_URL.rstrip("/")

        file_url = f"{media_base_url}/{obj.file.name}"

        if name.endswith(image_extensions):
            return format_html(
                '<a href="{}" target="_blank">'
                '<img src="{}" '
                'style="width:80px;height:55px;'
                'object-fit:contain;border:1px solid #777;'
                'border-radius:4px;" />'
                '</a>',
                file_url,
                file_url,
            )

        return format_html(
            '<a href="{}" target="_blank">Open</a>',
            file_url,
        )

        # except Exception:
        #     return "-"

    preview.short_description = "Preview"

    def delete_queryset(self, request, queryset):

        for obj in queryset:

            if obj.file:
                try:
                    obj.file.delete(save=False)
                except Exception:
                    pass

        queryset.delete()