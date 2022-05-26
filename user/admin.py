from django.contrib import admin
from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        "role",
        "email",
        "title",
        "is_blocked",
        "image_s3_path",
    )


admin.site.register(User, UserAdmin)
