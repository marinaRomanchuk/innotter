from django.db import models
from django.contrib.auth.models import AbstractUser

import page.models


class User(AbstractUser):
    class Roles(models.TextChoices):
        USER = "user"
        MODERATOR = "moderator"
        ADMIN = "admin"

    username = None
    email = models.EmailField(unique=True)
    image_s3_path = models.CharField(
        max_length=200, null=True, blank=True, validators=[page.models.validate_url]
    )
    role = models.CharField(max_length=9, choices=Roles.choices)

    title = models.CharField(max_length=80)
    is_blocked = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.email
