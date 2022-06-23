import urllib
import mimetypes
from datetime import datetime
from urllib.error import HTTPError, URLError

from django.core.exceptions import ValidationError
from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    def __str__(self):
        return self.name


def validate_url(url: str):
    try:
        urllib.request.urlopen(url)
    except (HTTPError, URLError):
        raise ValidationError("Invalid url.")

    try:
        if not mimetypes.MimeTypes().guess_type(url)[0].startswith("image"):
            raise ValidationError("Only images allowed.")
    except (IndexError, AttributeError):
        raise ValidationError("Only images allowed.")


class PageManager(models.Manager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(unblock_date=None)
            .exclude(unblock_date__lt=datetime.now())
        )


class Page(models.Model):
    name = models.CharField(max_length=80)
    uuid = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    tags = models.ManyToManyField("Tag", blank=True, related_name="pages")

    owner = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="pages"
    )
    followers = models.ManyToManyField("user.User", blank=True, related_name="follows")

    image = models.URLField(null=True, blank=True, validators=(validate_url,))

    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        "user.User", blank=True, related_name="requests"
    )

    unblock_date = models.DateTimeField(null=True, blank=True)

    objects = PageManager()

    class Meta:
        verbose_name = "Page"
        verbose_name_plural = "Pages"

    def __str__(self):
        return self.name


class Post(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=180)

    reply_to = models.ForeignKey(
        "Post", on_delete=models.SET_NULL, null=True, related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField("Page", blank=True, related_name="likes")

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.content
