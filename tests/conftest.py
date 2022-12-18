from rest_framework.test import APIClient
from test_users.factories import UserFactory
import pytest


@pytest.fixture
def client():
    """
    Client fixture for requests
    """
    return APIClient()


@pytest.fixture
def user_client(client: APIClient) -> APIClient:
    """
    User fixture
    Returns client with user authenticated via tokens
    """
    user = UserFactory()

    return client
