from rest_framework import serializers

from .models import Tag, Post, Page
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = ("name", "uuid", "tags_list", "followers_list", "description",
                  "owner", "image", "is_private", "unblock_date")


class PageListSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    tags_list = TagSerializer(source="tags", many=True, read_only=True)
    followers_list = UserSerializer(source="followers", many=True, read_only=True)

    class Meta:
        model = Page
        fields = ("name", "uuid", "tags_list", "followers_list", "description",
                  "owner", "image", "is_private", "unblock_date")


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ("page", "content", "reply_to", "created_at", "updated_at")


class PostListSerializer(serializers.ModelSerializer):
    page = PageSerializer(read_only=True)
    reply_to = PostSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ("page", "content", "reply_to", "created_at", "updated_at")
