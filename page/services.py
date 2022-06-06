from datetime import datetime
from django.db.models import QuerySet, Q

from .models import Page, Post
from user.models import User


class GetAcceptRefuseFollowerService:
    @staticmethod
    def get_dict_of_users_from_queryset(data: QuerySet) -> dict:
        result_dict = {}
        for i, j in enumerate(data):
            result_dict.update({i: j.id})
        return result_dict

    @staticmethod
    def get_list_of_followers(page: Page) -> dict:
        follow_requests_data = (
            GetAcceptRefuseFollowerService.get_dict_of_users_from_queryset(
                page.follow_requests.all()
            )
        )
        data = {"follow_requests": follow_requests_data}

        followers_data = GetAcceptRefuseFollowerService.get_dict_of_users_from_queryset(
            page.followers.all()
        )
        data.update({"followers": followers_data})
        return data

    @staticmethod
    def accept_single_request(follower_id: int, page: Page) -> None:
        page.followers.add(follower_id)
        page.follow_requests.remove(follower_id)
        page.save()

    @staticmethod
    def accept_follow_requests(page: Page) -> None:
        for i in page.follow_requests.all():
            GetAcceptRefuseFollowerService.accept_single_request(i, page)

    @staticmethod
    def refuse_follow_requests(follower_id: int, page: Page) -> None:
        page.follow_requests.remove(follower_id)
        page.save()


class PageService:
    @staticmethod
    def subscribe(user: User, page: Page) -> None:
        if page.is_private:
            page.follow_requests.add(user)
        else:
            page.followers.add(user)
        page.save()

    @staticmethod
    def block(page: Page, unblock_date: str) -> None:
        if unblock_date.lower() == "permanently":
            page.unblock_date = datetime.max
        else:
            page.unblock_date = unblock_date
        page.save()

    @staticmethod
    def add_tag(page: Page, tag_id: int) -> None:
        page.tags.add(tag_id)
        page.save()

    @staticmethod
    def remove_tag(page: Page, tag_id: int) -> None:
        page.tags.remove(tag_id)
        page.save()


class PostService:
    @staticmethod
    def get_feed(user: User) -> QuerySet:
        queryset = Post.objects.all()
        following: list = Page.objects.filter(
            Q(followers=user) | Q(owner=user)
        ).values_list("id", flat=True)
        queryset = queryset.filter(page__in=following)
        return queryset

    @staticmethod
    def get_dict_of_pages_from_queryset(data: QuerySet) -> dict:
        result_dict = {"count": data.count()}
        for i, j in enumerate(data):
            result_dict.update({i: j.id})
        return result_dict

    @staticmethod
    def set_like(post: Post, page_id: int) -> None:
        post.likes.add(page_id)
        post.save()

    @staticmethod
    def remove_like(post: Post, page_id: int) -> None:
        post.likes.remove(page_id)
        post.save()
