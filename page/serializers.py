from typing import Dict
from rest_framework import serializers

from .models import Tag, Post, Page
from user.serializers import UserSerializer


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["name"]

    def create(self, data: Dict[str, str]) -> Tag:
        tag = Tag.objects.create(name=data["name"])
        tag.save()
        return tag


class PageSerializer(serializers.ModelSerializer):
    tags_list = TagSerializer(source="tags", many=True, required=False)
    followers_list = UserSerializer(source="followers", many=True, required=False)

    class Meta:
        model = Page
        fields = ["name", "uuid", "tags_list", "followers_list", "description",
                  "owner", "image", "is_private", "unblock_date"]

    def create(self, data) -> Page:
        page = Page.objects.create(name=data["name"], uuid=data["uuid"], description=data["description"],
                                   is_private=data["is_private"], image=data["image"], owner=data["owner"])
        page.save()
        return page


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["page", "content", "reply_to", "created_at", "updated_at"]

    def create(self, data: Dict[str, str]) -> Post:
        post = Post.objects.create(page=data["page"], content=data["content"], reply_to=data["reply_to"])
        post.save()
        return post
