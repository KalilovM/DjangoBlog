import pytest
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.test import APIClient

from tests.test_user.factories import UserFactory


@pytest.mark.django_db
def test_new_user():
    assert True
