from factory.django import DjangoModelFactory
import pytest
from users.models import User


@pytest.mark.django_db
def test_user_creation(user_factory: DjangoModelFactory):
    """
    User creation test via
    username: fake_username
    email: fake_email
    password: jfmnf123
    """

    user: User = user_factory.create(role="student")
    user.set_password("jfmnf123")

    # Test for none values
    assert user.username is not None
    assert user.email is not None
    assert user.password is not None
    assert user.check_password("jfmnf123")
    assert user.role == "student"

    # Test for user model creation
    assert User.objects.count() == 1
