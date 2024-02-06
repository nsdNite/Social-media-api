from django.contrib import admin

from social_media.models import (
    Profile, Post, Comment
)

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
