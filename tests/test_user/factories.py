import factory
from faker import Faker
from django.contrib.auth.models import User


fake: Faker = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = fake.user_name()
    email = fake.email()
    password = "jfmnf123"
