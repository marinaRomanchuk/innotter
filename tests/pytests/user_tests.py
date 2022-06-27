import pytest

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from user.models import User
from user.factories import UserFactory, fake


@pytest.fixture(scope="function")
def user():
    return UserFactory()


@pytest.fixture(scope="function")
def another_user():
    return UserFactory(email=fake.email())


@pytest.fixture(scope="function")
def admin():
    return UserFactory(email=fake.email(), role=User.Roles.ADMIN)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def api_user_with_credentials(db, api_client, user):
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def api_another_user_with_credentials(db, api_client, another_user):
    api_client.force_authenticate(user=another_user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture
def api_admin_with_credentials(db, api_client, admin):
    api_client.force_authenticate(user=admin)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse("user-list")
    response = api_client.get(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_authorized_request(api_user_with_credentials):
    url = reverse("user-list")
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_detail(api_user_with_credentials, user):
    url = reverse("user-detail", kwargs={"pk": user.pk})
    response = api_user_with_credentials.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_update(api_user_with_credentials, user):
    url = reverse("user-detail", kwargs={"pk": user.pk})
    response = api_user_with_credentials.patch(url, {"title": fake.name()})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_signup(client):
    url = reverse("signup")
    response = client.post(url, {"email": fake.email(), "password": fake.password()})
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db(transaction=True)
def test_block(api_admin_with_credentials, user):
    url = reverse("user-block", kwargs={"pk": user.pk})
    response = api_admin_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert User.objects.get(pk=user.pk).is_blocked is True


@pytest.mark.django_db
def test_change_to_moderator(api_admin_with_credentials, user):
    url = reverse("user-moderator", kwargs={"pk": user.pk})
    response = api_admin_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert User.objects.get(pk=user.pk).role == User.Roles.MODERATOR


@pytest.mark.django_db
def test_change_to_admin(api_admin_with_credentials, user):
    url = reverse("user-admin", kwargs={"pk": user.pk})
    response = api_admin_with_credentials.post(url)
    assert response.status_code == status.HTTP_200_OK

    assert User.objects.get(pk=user.pk).role == User.Roles.ADMIN
