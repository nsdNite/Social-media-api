from django.contrib import admin

from social_media.models import (
    Profile, Post
)

admin.site.register(Profile)
admin.site.register(Post)