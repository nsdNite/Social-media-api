from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("social_media.urls", namespace="social_media")),
    path("api/user/", include("user.urls", namespace="user")),
]
