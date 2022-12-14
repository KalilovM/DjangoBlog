import factory
from faker import Faker
from django.contrib.auth.models import User
import pytest
from rest_framework.test import APIClient


fake: Faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()
    email = fake.email()
    password = "jfmnf123"


@pytest.fixture
def client():
    return APIClient()
