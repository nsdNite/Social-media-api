from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from social_media.models import Profile, Follow
from social_media.serializers import ProfileListSerializer, ProfileDetailSerializer, ProfileSerializer, \
    ProfilePicSerializer


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
