from celery import shared_task
from django.utils import timezone

from social_media.models import Post
from user.models import User


@shared_task
def create_scheduled_post(user_id, content, scheduled_time):
    """Task to create a post at scheduled time"""
    scheduled_time_utc = timezone.make_aware(scheduled_time)

    if timezone.now() >= scheduled_time_utc:
        return "Scheduled time is already passed."

    delay = (scheduled_time_utc - timezone.now()).total_seconds()
    create_post.apply_async((user_id, content), countdown=delay)

    return f"Post successfully scheduled for {scheduled_time_utc}."


@shared_task
def create_post(user_id, content):
    """
    Task to create a post.
    """
    user = User.objects.get(pk=user_id)
    Post.objects.create(user=user, content=content)
