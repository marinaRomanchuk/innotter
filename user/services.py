from datetime import datetime

from .models import User
from page.models import Page


class UserService:
    @staticmethod
    def block_users_pages(user: User) -> None:
        Page.objects.filter(owner=user).update(unblock_date=datetime.max)

    @staticmethod
    def block_user(user: User) -> None:
        user.is_blocked = True
        user.save()
        UserService.block_users_pages(user)

    @staticmethod
    def unblock_users_pages(user: User) -> None:
        Page.objects.filter(owner=user).update(unblock_date=None)

    @staticmethod
    def unblock_user(user: User) -> None:
        user.is_blocked = False
        user.save()
        UserService.unblock_users_pages(user)

    @staticmethod
    def create_admin(user: User) -> None:
        user.role = "admin"
        user.is_staff = True
        user.is_superuser = True
        user.save()

    @staticmethod
    def create_moderator(user: User) -> None:
        user.role = "moderator"
        user.save()
