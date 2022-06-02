from typing import Union

from django.core.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status


class GetAcceptRefuseFollower:
    @staticmethod
    def get_list_of_followers(page):
        data = {}
        follow_requests_data = {}
        for i, j in enumerate(page.follow_requests.all()):
            follow_requests_data.update({
                i: j.id
            })
        data.update({"follow_requests": follow_requests_data})

        followers_data = {}
        for i, j in enumerate(page.followers.all()):
            followers_data.update({
                i: j.id
            })
        data.update({"followers": followers_data})
        return data

    @staticmethod
    def accept_follow_requests(request, page):
        if page.is_private:
            accept_all: bool = request.GET.get("accept_all") == "true"
            if accept_all:
                for i in page.follow_requests.all():
                    page.followers.add(i)
                page.follow_requests.clear()

            try:
                follower_id: Union[int, None] = int(request.GET.get("follower_id"))
            except (ValueError, TypeError):
                follower_id = None

            if follower_id:
                page.followers.add(follower_id)
                page.follow_requests.remove(follower_id)

            page.save()

    @staticmethod
    def refuse_follow_requests(request, page):
        if page.is_private:
            refuse_all: bool = request.GET.get("refuse_all") == "true"
            if refuse_all:
                page.follow_requests.clear()

            try:
                follower_id: Union[int, None] = int(request.GET.get("follower_id"))
            except (ValueError, TypeError):
                follower_id = None

            if follower_id:
                page.follow_requests.remove(follower_id)

            page.save()

    @staticmethod
    def subscribe(request, page):
        if request.user == page.owner:
            return Response({"detail": "You don't have a permission to subscribe your page."},
                            status=status.HTTP_403_FORBIDDEN)
        if request.user in page.followers.all() or request.user in page.follow_requests.all():
            return Response({"detail": "You don't have a permission to subscribe page twice."},
                            status=status.HTTP_403_FORBIDDEN)

        if page.is_private:
            page.follow_requests.add(request.user)
        else:
            page.followers.add(request.user)
        page.save()

        return Response(status=status.HTTP_200_OK)

    @staticmethod
    def block(request, page):
        try:
            page.unblock_date = request.POST.get("unblock_date")
            page.save()
        except ValidationError:
            return Response({"detail": "Invalid data format"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)
