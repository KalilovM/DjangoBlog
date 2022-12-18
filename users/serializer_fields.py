from rest_framework import serializers
from typing import Any
from users.models import User


class CurrentUserSerializer(serializers.ModelSerializer):
    """
    Current user serializer
    """

    role = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "last_name",
            "first_name",
            "role",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_password(self, value: str) -> str:
        """
        Validate password
        """
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password must be at least 8 characters long"
            )
        return value
