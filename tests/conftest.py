import pytest
from pytest_factoryboy import register
from tests.test_user.factories import UserFactory

register(UserFactory)


@pytest.fixture
def new_user(db, user_factory: UserFactory):
    user = user_factory.build()
    return user
