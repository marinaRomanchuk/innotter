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
    def change_to_admin(user_id: int) -> None:
        User.objects.filter(pk=user_id).update(
            role=User.Roles.ADMIN, is_staff=True, is_superuser=True
        )

    @staticmethod
    def change_to_moderator(user_id: int) -> None:
        User.objects.filter(pk=user_id).update(
            role=User.Roles.MODERATOR, is_staff=False, is_superuser=False
        )
