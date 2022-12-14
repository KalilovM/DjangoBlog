import pytest
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient
from rest_framework.response import Response


@pytest.mark.django_db
def test_user_create_api()
