from rest_framework import serializers

from social_media.models import Profile, Follow, Post

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


class FollowingSerializer(serializers.ModelSerializer):
    following = serializers.CharField(source="followed.profile.displayed_name", read_only=True)

    class Meta:
        model = Follow
        fields = (
            "following",
        )


class FollowersSerializer(serializers.ModelSerializer):
    follower = serializers.CharField(source="follower.profile.displayed_name", read_only=True)

    class Meta:
        model = Follow
        fields = (
            "follower",
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
        following_profiles = obj.user.following.all()
        return FollowingSerializer(following_profiles, many=True).data

    def get_followers(self, obj):
        followers_profiles = obj.user.followers.all()
        return FollowersSerializer(followers_profiles, many=True).data


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


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "media",
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id",
            "user",
            "content",
            "created_at",
        )


class PostDetailSerializer(serializers.ModelSerializer):
    profile_name = serializers.CharField(source="user.profile.displayed_name", read_only=True)
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            "id",
            "profile_name",
            "content",
            "media",
            "created_at",
            "likes_count",
            "comments_count"
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()


class PostListSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    profile_name = serializers.CharField(source="user.profile.displayed_name", read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "profile_name",
            "content",
            "media",
            "created_at",
            "likes_count",
            "comments_count",
        )

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_comments_count(self, obj):
        return obj.comments.count()
