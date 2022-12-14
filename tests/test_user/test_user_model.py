from factory.django import DjangoModelFactory
import pytest
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_user_creation(user_factory: DjangoModelFactory):
    """
    User creation test via
    username: fake_username
    email: fake_email
    password: jfmnf123
    """

    user: User = user_factory.create()

    # Test for none values
    assert (
        user.username is not None
        and user.email is not None
        and user.check_password("jfmnf123")
        and user.first_name is not None
        and user.last_name is not None
    )
    # Test for user model creation
    assert User.objects.count() == 1
