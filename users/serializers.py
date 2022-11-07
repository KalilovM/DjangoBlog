from rest_framework import serializers
from .models import Profile

# To check firstly file then image
from drf_extra_fields.fields import HybridImageField
from django.utils.translation import gettext as _
from datetime import date
from typing import Union, OrderedDict
from dateutil.relativedelta import relativedelta

# The dateutil module provides powerful extensions to the standard datetime module, available in Python.
from posts.mixins import ErrorMessagesSerializerMixin
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
import re  # Regular expressions
from django.db.utils import IntegrityError
from django.utils import timezone


class CreateProfileSerializer(
    serializers.ModelSerializer, ErrorMessagesSerializerMixin
):
    avatar = HybridImageField(required=False, allow_null=True)
    email = serializers.EmailField(
        label="Адрес электронной почты", required=True, write_only=True
    )
    default_error_messages = {
        "invalid_image": serializers.ImageField.default_error_messages.get(
            "invalid_message",
            _("Файл который вы загрузили, поврежден или не является изображением"),
        ),
        "age_under_fourteen": _("Вам меньше 14 лет"),
        "age_more_than_hundred": _("Вы не можете указать возраст больше 100"),
        "cannot_create_user": _(
            "Не получилось создать пользователя, попробуйте снова."
        ),
        "username_contains_only_digits": {
            "username": _("Логин не может состоять только из цифр.")
        },
        "first_name_contains_digits": {
            "first_name": _("В имени не могут быть цифры."),
        },
        "last_name_contains_digits": {
            "last_name": _("В фамилии не могут быть цифры."),
        },
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["avatar"].error_messages[
            "invalid"
        ] = self.default_error_messages.get("invalid_image")

    def validate_birthday(self, value: date) -> Union[date, None]:
        today = timezone.now()

        if relativedelta(today, value).years < 14:
            self.fail("age_under_fourteen")

        if relativedelta(today, value).years > 100:
            self.fail("age_more_than_hundred")

        return value

    def validate_names(self, username: str, first_name: str, last_name: str) -> None:
        if username.isdigit():
            self.fail("username_contains_only_digits")
        if re.search(r"\d", first_name):
            self.fail("first_name_contains_digits")
        if re.search(r"\d", last_name):
            self.fail("last_name_contains_digits")

    def validate(self, attrs):
        username, first_name, last_name = (
            attrs.get("username"),
            attrs.get("first_name"),
            attrs.get("last_name"),
        )
        self.validate_names(username, first_name, last_name)
        return super().validate(attrs)

    class Meta:
        model = Profile
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "password",
            "is_active",
            "avatar",
            "birthday",
        ]
        extra_kwargs = {
            "birthday": {"required": True, "allow_null": False},
            "password": {"write_only": True, "validators": [validate_password]},
            "is_active": {"read_only": True},
            "username": {"max_length": 50, "min_length": 4},
            "first_name": {"required": True, "allow_blank": False, "max_length": 30},
            "last_name": {"required": True, "allow_blank": False, "max_length": 30},
        }


class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "username"]


class ProfileSerializer(serializers.ModelSerializer):
    followers = FollowerSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = [
            "email",
            "username",
            "first_name",
            "last_name",
            "followers",
            "is_active",
            "avatar",
            "birthday",
        ]
