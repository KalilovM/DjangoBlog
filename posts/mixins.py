from rest_framework import serializers
from rest_framework.settings import api_settings
from core.permissions import IsAuthorOrReadOnly
from rest_framework.serializers import Serializer
from rest_framework.response import Response
from typing import Type


class ErrorMessagesSerializerMixin:
    """
    A mixin for serializers that makes it easy to raise exceptions from default_error_messages.

    Made for the reason that the default self.fail() of serializers does
    not support errors in the form of dictionaries
    """

    def fail(self, key: str) -> None:
        """
        A helper method that simply rises a validation error
        """

        try:
            msg = self.error_messages[key]

        except KeyError:
            class_name = self.__class__.__name__
            msg = (
                f"Validation error rised by {class_name},"
                f"but error key `{key}` doesn't exists in the `error_messages` dictionary"
            )
            raise KeyError(msg)

        raise serializers.ValidationError(msg, code=key)


class IsAuthorPermissionsMixin:
    """
    Adds IsAuthorOrReadOnly permission
    """

    permission_classes = api_settings.DEFAULT_PERMISSION_CLASSES + [IsAuthorOrReadOnly]


class CacheTreeQuerysetMixin:
    """
    A mixin that caches the list of records obtained via mptt.get_cached_trees
    into the _cached_queryset attribute.
    Otherwise, two identical queries will be executed
    Supported depth attribute which specifies the length of mptt descendants
    """

    _cached_queryset: list | None = None
    depth: int | None = None

    def _get_cached_queryset(self, queryset):

        if self.depth:
            queryset = queryset.filter(level__lte=self.depth)

        if not self._cached_queryset:
            self._cached_queryset = get_cached_trees(queryset)

        return self._cached_queryset


class LikeMixin:
    """
    A mixin that works with m2m field (lookup field) of the model, providing the functionality of likes
    """

    lookup_method: str | None = None
    instance_name: str | None = None
    serializer_class: Type[Serializer] | None = None

    def like(self, request) -> Response:
        """
        Accept request data to serializer_class, validate it, takes instance by the instance_name key from the validated data,
        filters the m2m instance lookup_field, if there is already a like, removes it, if not yet, adds it.
        Response: action that shows what should be done, remove the like - or add.
        """

        serializer: Serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        instance = data.get(self.instance_name)
        instance_like_method = getattr(instance, self.lookup_method, None)

        if not instance_like_method:
            raise AttributeError(
                f"<{instance.__class__.__name__}> object has no attribute <{self.lookup_method}>."
            )

        user = request.user
        is_like = instance_like_method(user)

        if is_like:
            return Response(data={"action": "add"}, status=200)

        else:
            return Response(data={"action": "remove"}, status=200)
