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


def profile_pic_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.displayed_name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/user_pics/", filename)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    displayed_name = models.CharField(max_length=60, unique=True, blank=False)
    bio = models.TextField(max_length=500, blank=True)
    profile_pic = models.ImageField(null=True, upload_to=profile_pic_file_path, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["date_joined"]

    def follow(self, other_user):
        follow_obj, created = Follow.objects.get_or_create(
            follower=self.user,
            followed=other_user,
        )

        return follow_obj

    def __str__(self):
        return self.displayed_name


def media_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.created_at)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/post_media/", filename)


class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    media = models.ImageField(upload_to=media_file_path, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Post by {self.user.profile.displayed_name} on {self.created_at}"


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user.profile.displayed_name} liked {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", null=True, blank=True)
    text = models.TextField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.user.profile.displayed_name} on {self.post}"
