import factory
from faker import Faker

from user.factories import UserFactory


fake = Faker()


class TagFactory(factory.django.DjangoModelFactory):
    name = fake.word()

    class Meta:
        model = "page.Tag"


class PageFactory(factory.django.DjangoModelFactory):
    name = fake.word()
    owner = factory.SubFactory(UserFactory)
    uuid = fake.word()
    description = fake.text()
    is_private = False

    class Meta:
        model = "page.Page"


class PostFactory(factory.django.DjangoModelFactory):
    content = fake.word()
    page = factory.SubFactory(PageFactory)

    class Meta:
        model = "page.Post"
