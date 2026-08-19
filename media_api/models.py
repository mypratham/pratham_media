from django.db import models


class MediaFile(models.Model):
    file = models.FileField(
        upload_to="admin_uploads/",
        verbose_name="File"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Media"
        verbose_name_plural = "Media"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.file.name