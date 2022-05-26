from django.contrib import admin
from .models import Post, Tag, Page


class TagAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "page",
        "content",
        "reply_to",
        "created_at",
        "updated_at",
    )


class PageAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "uuid",
        "description",
        "owner",
        "image",
        "is_private",
        "unblock_date",
    )


admin.site.register(Tag, TagAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Post, PostAdmin)
