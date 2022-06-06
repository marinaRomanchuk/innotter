from .models import User
from page.models import Page
from page.services import PageService


class UserService:
    @staticmethod
    def block_users_pages(user: User) -> None:
        pages_to_block = Page.objects.filter(owner=user)
        for page in pages_to_block:
            PageService.block(page, "permanently")

    @staticmethod
    def block_user(user: User) -> None:
        user.is_blocked = True
        user.save()
        UserService.block_users_pages(user)

    @staticmethod
    def unblock_users_pages(user: User) -> None:
        pages_to_unblock = Page.objects.filter(owner=user)
        for page in pages_to_unblock:
            page.unblock_date = None
            page.save()

    @staticmethod
    def unblock_user(user: User) -> None:
        user.is_blocked = False
        user.save()
        UserService.unblock_users_pages(user)
