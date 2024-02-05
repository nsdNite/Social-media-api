from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_media.models import Profile, Follow, Post
from social_media.serializers import ProfileListSerializer, ProfileDetailSerializer, ProfileSerializer, \
    ProfilePicSerializer, PostSerializer, PostListSerializer, PostDetailSerializer, PostMediaSerializer


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ProfileListSerializer

        if self.action == "retrieve":
            return ProfileDetailSerializer

        if self.action == "upload_image":
            return ProfilePicSerializer

        return ProfileSerializer

    def get_queryset(self):
        """Retrieve profile by displayed name"""
        displayed_name = self.request.query_params.get("displayed_name")
        queryset = self.queryset

        if displayed_name:
            queryset = queryset.filter(displayed_name__icontains=displayed_name)

        return queryset.distinct()

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["POST"],
        detail=True,
        url_path="follow",
    )
    def follow_profile(self, request, pk=None):
        """Endpoint for following user"""
        profile_to_follow = self.get_object()
        request_user_profile = self.request.user.profile
        request_user_profile.follow(profile_to_follow.user)

        return Response({'detail': 'Successfully followed.'}, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=True,
        url_path="unfollow",
    )
    def unfollow_profile(self, request, pk=None):
        """Endpoint for unfollowing user"""
        profile_to_unfollow = self.get_object()
        request_user_profile = self.request.user.profile

        try:
            follow_obj = Follow.objects.get(
                follower=request_user_profile.user,
                followed=profile_to_unfollow.user,
            )
            follow_obj.delete()
            return Response({'detail': 'Successfully unfollowed.'}, status=status.HTTP_200_OK)
        except Follow.DoesNotExist:
            return Response({'detail': 'You are not following this profile.'}, status=status.HTTP_400_BAD_REQUEST)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        if self.action == "retrieve":
            return PostDetailSerializer
        if self.action == "upload_media":
            return PostMediaSerializer

        return PostSerializer

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload-media",
    )
    def upload_media(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["GET"],
        detail=False,  # Not related to a specific post
        url_path="user-posts",
    )
    def user_posts(self, request):
        """Endpoints for posts made by the current user"""
        user = self.request.user
        posts = Post.objects.filter(user=user).order_by('-created_at')
        serializer = PostListSerializer(posts, many=True)
        return Response(serializer.data)

    @action(
        methods=["GET"],
        detail=False,
        url_path="following-posts",
    )
    def following_posts(self, request):
        """Endpoint for posts made by users that the current user is following"""
        user = self.request.user
        following_users = Follow.objects.filter(follower=user).values_list('followed', flat=True)
        following_posts = Post.objects.filter(user__in=following_users).order_by('-created_at')
        serializer = PostListSerializer(following_posts, many=True)
        return Response(serializer.data)
