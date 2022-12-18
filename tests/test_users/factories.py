import factory
from faker import Faker
from users.models import User

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
