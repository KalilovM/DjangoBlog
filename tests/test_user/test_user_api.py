from django.urls import reverse
from typing import Dict
from users.models import User
import pytest
from factory.django import DjangoModelFactory
from rest_framework.test import APIClient
from rest_framework.response import Response

pytestmark = pytest.mark.django_db


class TestAuthUser:
    """
    Test for user authentication
    """

    def test_user_creation(
        self, user_factory: DjangoModelFactory, client: APIClient
    ) -> None:
        # Checking user creation
        payload: Dict = dict(
            username="testinguser",
            email="testinguser@test.com",
            password="testinguser",
        )
        response: Response = client.post(reverse("user-create"), payload)
        assert response.status_code == 201
        assert response.data["username"] == payload["username"]
        assert response.data["email"] == payload["email"]
        assert response.data["role"] == "student"
        with pytest.raises(KeyError):
            # Password should not be returned
            response.data["password"]

    def test_user_creation_with_invalid_data(
        self,
        user_factory: DjangoModelFactory,
        client: APIClient,
    ) -> None:
        # Checking validation errors
        user: User = user_factory.create(
            username="testinguser", email="testinguser@gmail.com", password="jfmnf123"
        )
        payload: Dict = dict(
            username="testinguser",
            email="testinguser@gmail.com",
            password="123jf",
        )
        response: Response = client.post(reverse("user-create"), payload)
        assert response.status_code == 400
        assert (
            response.data["username"][0] == "A user with that username already exists."
        )
        assert (
            response.data["email"][0] == "User with this Email address already exists."
        )
        assert (
            response.data["password"][0]
            == "Password must be at least 8 characters long"
        )

    def test_user_login(self, client: APIClient):
        # Checking user login
        payload: Dict = dict(
            username="testinguser",
            email="testinguser@test.com",
            password="testinguser",
        )
        response: Response = client.post(reverse("user-create"), payload)
        assert response.status_code == 201
        assert response.data["username"] == payload["username"]
        assert response.data["email"] == payload["email"]
        assert response.data["role"] == "student"
        with pytest.raises(KeyError):
            # Password should not be returned
            response.data["password"]
        response: Response = client.post(reverse("token-get"), payload)
        assert response.status_code == 200
        assert response.data["access"] is not None
        assert response.data["refresh"] is not None
