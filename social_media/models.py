import os
import uuid

from django.db import models
from django.utils.text import slugify

from social_media_service import settings


class Follow(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="following")
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followers")

    class Meta:
        unique_together = ("follower", "followed")

    def __str__(self):
        return f"{self.follower} follows {self.followed}"


def profile_pic_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    displayed_name = models.CharField(max_length=60, unique=True)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(null=True, upload_to=profile_pic_file_path)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["date_joined"]

    def __str__(self):
        return self.displayed_name
