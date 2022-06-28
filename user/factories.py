import factory
from faker import Faker

from .models import User


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    email = fake.email()
    password = fake.password()
    role = User.Roles.USER

    class Meta:
        model = "user.User"
