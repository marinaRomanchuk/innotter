import pytest

from django.urls import reverse
from rest_framework import status

from page.models import Post, Page
from .user_tests import (
    user,
    another_user,
    admin,
    api_admin_with_credentials,
    api_user_with_credentials,
    api_client,
    api_another_user_with_credentials,
)
from page.factories import TagFactory, PageFactory, PostFactory, fake


@pytest.fixture(scope="function")
def tag():
    return TagFactory()


@pytest.fixture(scope="function")
def page(user):
    return PageFactory(owner=user)


@pytest.fixture(scope="function")
def private_page(another_user):
    return PageFactory(is_private=True, owner=another_user)


@pytest.fixture(scope="function")
def post(page):
    return PostFactory(page=page)


@pytest.fixture(scope="function")
def post_on_private_page(db, private_page):
    return PostFactory(page=private_page)


@pytest.mark.django_db
def test_page_creation(api_user_with_credentials, user):
    url = reverse("page-list")
    data = {
        "name": fake.word(),
        "owner": user.pk,
        "uuid": fake.word(),
        "description": fake.text(),
    }
    response = api_user_with_credentials.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_post_creation(api_user_with_credentials, page):
    url = reverse("post-list")
    data = {"content": fake.word(), "page": page.pk}
    response = api_user_with_credentials.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_add_tag(api_user_with_credentials, page, tag):
    url = reverse("tag-detail", kwargs={"page_pk": page.pk, "pk": tag.pk})
    response = api_user_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert tag in Page.objects.get(pk=page.pk).tags.all()


@pytest.mark.django_db(transaction=True)
def test_add_follower(api_another_user_with_credentials, page, another_user):
    url = reverse("page-subscribe", kwargs={"pk": page.pk})
    response = api_another_user_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert another_user in Page.objects.get(pk=page.pk).followers.all()


@pytest.mark.django_db(transaction=True)
def test_add_follower_to_private_page(api_user_with_credentials, private_page, user):
    url = reverse("page-subscribe", kwargs={"pk": private_page.pk})
    response = api_user_with_credentials.post(url)

    assert response.status_code == status.HTTP_200_OK

    assert user in Page.objects.get(pk=private_page.pk).follow_requests.all()


@pytest.mark.django_db
def test_get_followers(api_user_with_credentials, page):
    url = reverse("followers-list", kwargs={"page_pk": page.pk})
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_accept_follower(api_another_user_with_credentials, private_page, user):
    page = Page.objects.get(pk=private_page.pk)
    page.follow_requests.add(user.id)
    page.save()

    url = reverse(
        "followers-detail", kwargs={"page_pk": private_page.pk, "pk": user.pk}
    )
    response = api_another_user_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert user in Page.objects.get(pk=private_page.pk).followers.all()


@pytest.mark.django_db
def test_accept_all_followers(api_another_user_with_credentials, private_page, user):
    page = Page.objects.get(pk=private_page.pk)
    page.follow_requests.add(user.id)
    page.save()

    url = reverse("followers-list", kwargs={"page_pk": private_page.pk})
    response = api_another_user_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert user in Page.objects.get(pk=private_page.pk).followers.all()


@pytest.mark.django_db
def test_refuse_follower(api_another_user_with_credentials, private_page, user):
    page = Page.objects.get(pk=private_page.pk)
    page.follow_requests.add(user.id)
    page.save()

    url = reverse(
        "followers-detail", kwargs={"page_pk": private_page.pk, "pk": user.pk}
    )
    response = api_another_user_with_credentials.delete(url)
    assert response.status_code == status.HTTP_200_OK

    assert user not in Page.objects.get(pk=private_page.pk).followers.all()
    assert user not in Page.objects.get(pk=private_page.pk).follow_requests.all()


@pytest.mark.django_db
def test_not_follower_get_private_page(api_user_with_credentials, private_page, user):
    url = reverse("page-detail", kwargs={"pk": private_page.pk})
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_follower_get_private_page(api_user_with_credentials, private_page, user):
    page = Page.objects.get(pk=private_page.pk)
    page.followers.add(user.id)
    page.save()

    url = reverse("page-detail", kwargs={"pk": private_page.pk})
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_follower_patch_page(api_another_user_with_credentials, page, another_user):
    page = Page.objects.get(pk=page.pk)
    page.followers.add(another_user.id)
    page.save()

    url = reverse("page-detail", kwargs={"pk": page.pk})
    response = api_another_user_with_credentials.patch(url, {"name": "new"})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_owner_patch_page(api_user_with_credentials, page):
    url = reverse("page-detail", kwargs={"pk": page.pk})
    response = api_user_with_credentials.patch(url, {"name": "new"})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_get_liked_posts(api_another_user_with_credentials, private_page, post):
    post = Post.objects.get(pk=post.pk)
    post.likes.add(private_page.pk)
    post.save()

    url = reverse("page-liked", kwargs={"pk": private_page.pk})
    response = api_another_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_like_post(api_user_with_credentials, post, page):
    url = reverse("like-detail", kwargs={"post_pk": post.pk, "pk": page.pk})
    response = api_user_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert page in Post.objects.get(pk=post.pk).likes.all()


@pytest.mark.django_db(transaction=True)
def test_like_post_on_private_page(
    api_user_with_credentials, post_on_private_page, page
):
    url = reverse(
        "like-detail", kwargs={"post_pk": post_on_private_page.pk, "pk": page.pk}
    )
    response = api_user_with_credentials.post(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_unlike_post(api_user_with_credentials, post, page):
    post = Post.objects.get(pk=post.pk)
    post.likes.add(page.pk)
    post.save()

    url = reverse("like-detail", kwargs={"post_pk": post.pk, "pk": page.pk})
    response = api_user_with_credentials.delete(url)
    assert response.status_code == status.HTTP_200_OK

    assert page not in Post.objects.get(pk=post.pk).likes.all()


@pytest.mark.django_db
def test_get_likes_on_post(api_user_with_credentials, post):
    url = reverse("like-list", kwargs={"post_pk": post.pk})
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_get_likes_on_post_from_private_page(
    api_user_with_credentials, post_on_private_page
):
    url = reverse("like-list", kwargs={"post_pk": post_on_private_page.pk})
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_search(api_user_with_credentials, another_user):
    url = reverse("search-list")
    response = api_user_with_credentials.get(url, {"search": "another"})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db(transaction=True)
def test_block_page(api_admin_with_credentials, page):
    url = reverse("page-block", kwargs={"pk": page.pk})
    response = api_admin_with_credentials.post(
        url, {"unblock_date": "2022-06-27 10:20:09.184106+00:00"}
    )
    assert response.status_code == status.HTTP_200_OK
