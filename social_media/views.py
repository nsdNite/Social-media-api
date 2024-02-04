from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response

from social_media.models import Profile
from social_media.serializers import ProfileListSerializer, ProfileDetailSerializer, ProfileSerializer, ProfilePicSerializer


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

    def upload_image(self, request, pk=None):
        """Endpoint for uploading image to specific movie"""
        profile = self.get_object()
        serializer = self.get_serializer(profile, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)