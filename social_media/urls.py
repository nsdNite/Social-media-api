from django.urls import path
from rest_framework.routers import DefaultRouter

from social_media.views import (
    ProfileViewSet,
    PostViewSet,
    CommentViewSet,
    ScheduledPostViewSet,
)

router = DefaultRouter()
router.register(r"profiles", ProfileViewSet)
router.register(r"posts", PostViewSet)
router.register(
    r"posts/(?P<post_pk>\d+)/comments", CommentViewSet, basename="comments"
)
router.register(
    r"scheduled-posts", ScheduledPostViewSet, basename="scheduled-posts"
)

urlpatterns = router.urls

app_name = "social_media"
