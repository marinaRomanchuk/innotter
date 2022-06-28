import factory
from factory import lazy_attribute
from faker import Faker

from user.factories import UserFactory


fake = Faker()


class TagFactory(factory.django.DjangoModelFactory):
    name = fake.word()

    class Meta:
        model = "page.Tag"


class PageFactory(factory.django.DjangoModelFactory):
    name = lazy_attribute(lambda a: fake.word())
    owner = factory.SubFactory(UserFactory)
    uuid = lazy_attribute(lambda a: fake.word())
    description = lazy_attribute(lambda a: fake.text())
    is_private = False

    class Meta:
        model = "page.Page"


class PostFactory(factory.django.DjangoModelFactory):
    content = lazy_attribute(lambda a: fake.word())
    page = factory.SubFactory(PageFactory)

    class Meta:
        model = "page.Post"
