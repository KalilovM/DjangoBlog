from rest_framework import serializers
from .models import Links


class LinkSerializer(serializers.Serializer):
    """
    Link serializer
    """

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Links
        fields = ["network", "contact"]
