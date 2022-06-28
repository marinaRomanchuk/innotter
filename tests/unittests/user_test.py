from django.contrib.auth.hashers import make_password
from rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status
from user.models import User
from faker import Faker

fake = Faker()


class UserTest(APITestCase):
    def setUp(self):
        self.email = fake.email()
        self.password = fake.password()
        self.signup_data = {"email": self.email, "password": self.password}
        self.data = {
            "email": self.email,
            "role": "user",
            "image_s3_path": None,
            "title": "",
            "is_blocked": False,
        }
        self.user = User.objects.create(
            email=self.email,
            password=make_password(self.password),
            role=User.Roles.USER,
        )

    def authenticate(self, login_data):
        url = reverse("login")
        response = self.client.post(url, login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        token = response.data["access"]
        self.credentials = f"Token {token}"
        self.client.credentials(HTTP_AUTHORIZATION=self.credentials)

    def test_signup(self):
        email = fake.email()
        response = self.client.post(
            reverse("signup"), {"email": email, "password": fake.password()}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), {"email": email})

    def test_cannot_signup(self):
        response = self.client.post(
            reverse("signup"), {"email": fake.email(), "password": "12345"}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_retrieve_self_user(self):
        self.authenticate(self.signup_data)
        response = self.client.get(reverse("user-detail", kwargs={"pk": self.user.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(response.json(), self.data)

    def test_can_patch_self_user(self):
        self.authenticate(self.signup_data)
        response = self.client.patch(
            reverse("user-detail", kwargs={"pk": self.user.pk}), {"title": fake.word()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
