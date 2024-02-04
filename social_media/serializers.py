from rest_framework import serializers

from social_media.models import Profile

from user.serializers import UserSerializer


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
    following = serializers.SerializerMethodField()
    followers = serializers.SerializerMethodField()

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
            "followers",
        )

    def get_following(self, obj):
        following_users = obj.user.following.all()
        return ProfileSerializer(following_users, many=True).data

    def get_followers(self, obj):
        followers_users = obj.user.followers.all()
        return ProfileSerializer(followers_users, many=True).data


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
        return obj.user.following.count()

    def get_followers_count(self, obj):
        return obj.user.followers.count()
