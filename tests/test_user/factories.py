import factory
from faker import Faker
from users.models import User
import pytest
from rest_framework.test import APIClient


fake: Faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    """
    User factory
    """

    class Meta:
        model = User

    username = fake.user_name()
    email = fake.email()
    password = "jfmnf123"


@pytest.fixture
def client():
    """
    Client fixture for requests
    """
    return APIClient()
