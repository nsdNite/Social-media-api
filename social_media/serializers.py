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
    following = serializers.StringRelatedField(many=True)
    followers = serializers.StringRelatedField(many=True)

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
            "following",
            "followers"
        )


class ProfileListSerializer(serializers.ModelSerializer):
    following_count = serializers.SerializerMethodField()
    followers_count = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = (
            "id",
            "displayed_name",
            "profile_pic",
            "date_joined",
            "following_count",
            "followers_count",
        )

    def get_following_count(self, obj):
        return obj.following.count()

    def get_followers_count(self, obj):
        return obj.user.followers.count()
