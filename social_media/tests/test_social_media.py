from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from social_media.models import Post
from social_media.serializers import PostSerializer, PostListSerializer

PROFILE_URL = reverse("social_media:profile-list")
POST_URL = reverse("social_media:post-list")


class UnauthenticatedSocialMediaTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PROFILE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedSocialMediaTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test_password12345",
        )
        self.client.force_authenticate(self.user)

    def sample_post(self, **params):
        """Define sample instance of Post model"""
        defaults = {
            "user": self.user,
            "content": "Test post content",
        }
        defaults.update(params)

        return Post.objects.create(**defaults)

    def test_list_post(self):
        self.sample_post()

        res = self.client.get(POST_URL)

        posts = Post.objects.all()
        serializer = PostListSerializer(posts, many=True)
        print(res.data)
        print(serializer.data)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_posts_by_hashtag(self):
        post_1 = self.sample_post(content="Test post #1")
        post_2 = self.sample_post(content="Test post #11")
        post_3 = self.sample_post(content="Test post #3")

        # Filter by existing hashtag
        res = self.client.get(POST_URL, {"hashtag": "1"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data[0]['content'], "Test post #1")
        self.assertEqual(res.data[1]['content'], "Test post #11")

        # Filter by non-existing hashtag
        res = self.client.get(POST_URL, {"hashtag": "99"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

        # Filter without providing hashtag
        res = self.client.get(POST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 3)  # All posts should be returned
