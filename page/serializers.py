from rest_framework import serializers

from .models import Tag, Post, Page
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            "id",
            "name"
        )


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            "name",
            "uuid",
            "tags",
            "followers",
            "follow_requests",
            "description",
            "owner",
            "image",
            "is_private",
            "unblock_date"
        )


class PageListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    followers = UserSerializer(many=True, read_only=True)
    follow_requests = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Page
        fields = (
            "name",
            "uuid",
            "tags",
            "followers",
            "follow_requests",
            "description",
            "owner",
            "image",
            "is_private",
            "unblock_date"
        )


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "page",
            "content",
            "reply_to",
            "created_at",
            "updated_at"
        )


class PostListSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)
    reply_to = PostSerializer(read_only=True)

    class Meta:
        model = Post
        fields = (
            "page",
            "content",
            "reply_to",
            "created_at",
            "updated_at"
        )
