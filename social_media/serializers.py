from rest_framework import serializers

from social_media.models import Profile
from social_media_service import settings


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = settings.AUTH_USER_MODEL
        fields = (
            "username",
            "email",
        )


class ProfilePicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "profile_pic",
        )


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "displayed_name",
            "bio",
            "date_joined",
            "date_of_birth",
        )


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "user",
            "displayed_name",
            "bio",
            "profile_pic",
            "date_joined",
            "date_of_birth",
        )


class ProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = (
            "id",
            "displayed_name",
            "profile_pic",
            "date_joined"
        )
