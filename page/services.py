from typing import Union


class GetAcceptRefuseFollowerService:
    @staticmethod
    def get_dict_of_users_from_queryset(data) -> dict:
        result_dict = {}
        for i, j in enumerate(data):
            result_dict.update({i: j.id})
        return result_dict

    @staticmethod
    def get_list_of_followers(page):
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
    def accept_single_request(follower_id: int, page):
        page.followers.add(follower_id)
        page.follow_requests.remove(follower_id)

    @staticmethod
    def accept_follow_requests(accept_all: bool, follower_id: Union[int, None], page):
        if accept_all:
            for i in page.follow_requests.all():
                GetAcceptRefuseFollowerService.accept_single_request(i, page)

        if follower_id:
            GetAcceptRefuseFollowerService.accept_single_request(follower_id, page)

        page.save()

    @staticmethod
    def refuse_follow_requests(refuse_all: bool, follower_id: Union[int, None], page):
        if refuse_all:
            page.follow_requests.clear()

        if follower_id:
            page.follow_requests.remove(follower_id)

        page.save()

    @staticmethod
    def subscribe(user, page):
        if page.is_private:
            page.follow_requests.add(user)
        else:
            page.followers.add(user)
        page.save()

    @staticmethod
    def block(page, unblock_date):
        page.unblock_date = unblock_date
        page.save()
