from typing import TypeVar, Type
from rest_framework import serializers
from users.models import Profile
from drf_spectacular.utils import extend_schema_field
from rest_framework.fields import empty


class AuthorSerializer(serializers.ModelSerializer):
    """Serializers of the data required to represent the author"""

    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        field = serializers.ImageField()
        field.bind("avatar", self)
        return field.to_representation(obj.avatar)

    class Meta:
        model = Profile
        fields = ["avatar", "username"]


@extend_schema_field(
    {
        "type": "string",
        "format": "string",
        "read_only": True,
        "example": {
            "first_name": "string",
            "last_name": "string",
            "avatar": "string",
        },
    }
)
class CurrentAuthorField(serializers.Field):
    """
    The author field, which requires the Profile object at the input and returns the author's data for it.
    Ignores any input value, focusing only on the default view
    """

    T = TypeVar("T")

    def get_value(self, dictionary: dict) -> Type[empty]:
        return serializers.empty

    def to_representation(self, value: Profile) -> dict:
        """To JSON"""
        return AuthorSerializer(
            instance=value, context={"request": self.context.get("request")}
        ).data

    def to_internal_value(self, data: T) -> T:
        return data
