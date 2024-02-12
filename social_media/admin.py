from django.contrib import admin

from social_media.models import Profile, Post, Comment, ScheduledPost, Like, Follow

admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(ScheduledPost)
admin.site.register(Like)
admin.site.register(Follow)
